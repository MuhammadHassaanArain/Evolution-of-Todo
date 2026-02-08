import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from unittest.mock import patch
from datetime import datetime
import sys
import os

# Add the backend/src to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from backend.src.main import app
from backend.src.database.connection import engine, create_db_and_tables
from backend.src.models.user import User
from backend.src.models.todo import Todo
from backend.src.services.todo_service import TodoService
from backend.src.api.deps import get_current_user


@pytest.fixture(scope="module")
def client():
    """
    Create a test client for the API.
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def setup_test_db():
    """
    Set up the test database with tables.
    """
    create_db_and_tables()
    yield
    # Clean up after tests if needed


def mock_get_current_user():
    """
    Mock function to return a test user.
    """
    return User(
        id=1,
        email="test@example.com",
        username="testuser",
        hashed_password="fakehashedpassword",
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@pytest.mark.parametrize("endpoint,method", [
    ("/api/v1/todos", "POST"),
    ("/api/v1/todos", "GET"),
    ("/api/v1/todos/1", "GET"),
    ("/api/v1/todos/1", "PUT"),
    ("/api/v1/todos/1", "DELETE")
])
def test_endpoints_require_authentication(client, endpoint, method):
    """
    Test that all endpoints require authentication.
    """
    if method == "POST":
        response = client.post(endpoint, json={})
    elif method == "GET":
        response = client.get(endpoint)
    elif method == "PUT":
        response = client.put(endpoint, json={})
    elif method == "DELETE":
        response = client.delete(endpoint)

    # All endpoints should return 401 for unauthenticated requests
    assert response.status_code == 401


def test_full_todo_lifecycle_with_auth(client):
    """
    Integration test for the complete Todo lifecycle with authentication.
    """
    # Mock the authentication dependency
    app.dependency_overrides[get_current_user] = mock_get_current_user

    try:
        # 1. Create a todo
        create_response = client.post(
            "/api/v1/todos",
            json={
                "title": "Integration Test Todo",
                "description": "A todo created during integration testing",
                "is_completed": False
            }
        )
        assert create_response.status_code == 201
        created_todo = create_response.json()
        assert created_todo["title"] == "Integration Test Todo"
        assert created_todo["owner_id"] == 1  # From mock user
        assert "id" in created_todo

        todo_id = created_todo["id"]

        # 2. Get the created todo
        get_response = client.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == 200
        retrieved_todo = get_response.json()
        assert retrieved_todo["id"] == todo_id
        assert retrieved_todo["title"] == "Integration Test Todo"

        # 3. Update the todo
        update_response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={
                "title": "Updated Integration Test Todo",
                "is_completed": True
            }
        )
        assert update_response.status_code == 200
        updated_todo = update_response.json()
        assert updated_todo["id"] == todo_id
        assert updated_todo["title"] == "Updated Integration Test Todo"
        assert updated_todo["is_completed"] is True

        # 4. Get all todos for the user (should include our updated todo)
        list_response = client.get("/api/v1/todos")
        assert list_response.status_code == 200
        todos_list = list_response.json()
        assert isinstance(todos_list, list)
        assert len(todos_list) >= 1

        # Find our todo in the list
        our_todo = next((t for t in todos_list if t["id"] == todo_id), None)
        assert our_todo is not None
        assert our_todo["title"] == "Updated Integration Test Todo"
        assert our_todo["is_completed"] is True

        # 5. Delete the todo
        delete_response = client.delete(f"/api/v1/todos/{todo_id}")
        assert delete_response.status_code == 204  # Successful deletion returns 204

        # 6. Verify the todo is gone
        get_deleted_response = client.get(f"/api/v1/todos/{todo_id}")
        assert get_deleted_response.status_code == 404

    finally:
        # Remove the mock
        app.dependency_overrides.pop(get_current_user, None)


def test_user_isolation(client):
    """
    Test that users can only access their own todos.
    """
    # Mock the authentication for first user
    def mock_first_user():
        return User(
            id=1,
            email="first@example.com",
            username="firstuser",
            hashed_password="fakehashedpassword",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    def mock_second_user():
        return User(
            id=2,
            email="second@example.com",
            username="seconduser",
            hashed_password="fakehashedpassword",
            is_active=True,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

    # First, create a todo for the first user
    app.dependency_overrides[get_current_user] = mock_first_user

    try:
        # Create a todo for first user
        create_response = client.post(
            "/api/v1/todos",
            json={
                "title": "First User's Todo",
                "description": "Owned by first user",
                "is_completed": False
            }
        )
        assert create_response.status_code == 201
        first_user_todo = create_response.json()
        assert first_user_todo["owner_id"] == 1
        first_todo_id = first_user_todo["id"]

        # Switch to second user
        app.dependency_overrides[get_current_user] = mock_second_user

        # Second user should not be able to access first user's todo
        get_response = client.get(f"/api/v1/todos/{first_todo_id}")
        assert get_response.status_code == 404  # Not found (actually forbidden but returns 404 for security)

        # Second user should be able to create their own todo
        create_second_response = client.post(
            "/api/v1/todos",
            json={
                "title": "Second User's Todo",
                "description": "Owned by second user",
                "is_completed": False
            }
        )
        assert create_second_response.status_code == 201
        second_user_todo = create_second_response.json()
        assert second_user_todo["owner_id"] == 2
        second_todo_id = second_user_todo["id"]

        # Second user should be able to access their own todo
        get_second_response = client.get(f"/api/v1/todos/{second_todo_id}")
        assert get_second_response.status_code == 200
        retrieved_second_todo = get_second_response.json()
        assert retrieved_second_todo["id"] == second_todo_id
        assert retrieved_second_todo["owner_id"] == 2

        # Second user should still not be able to access first user's todo
        get_first_as_second_response = client.get(f"/api/v1/todos/{first_todo_id}")
        assert get_first_as_second_response.status_code == 404

    finally:
        # Remove the mock
        app.dependency_overrides.pop(get_current_user, None)


def test_validation_errors(client):
    """
    Test that validation errors are properly handled.
    """
    app.dependency_overrides[get_current_user] = mock_get_current_user

    try:
        # Try to create a todo with an empty title (should fail validation)
        invalid_create_response = client.post(
            "/api/v1/todos",
            json={
                "title": "",  # Empty title should fail validation
                "description": "This should not be created",
                "is_completed": False
            }
        )
        assert invalid_create_response.status_code == 422  # Validation error

        # Try to create a todo with a title that's too long
        long_title = "A" * 256  # Exceeds max length of 255
        invalid_long_response = client.post(
            "/api/v1/todos",
            json={
                "title": long_title,
                "description": "This should not be created due to long title",
                "is_completed": False
            }
        )
        assert invalid_long_response.status_code == 422  # Validation error

    finally:
        app.dependency_overrides.pop(get_current_user, None)


def test_database_consistency(client):
    """
    Test that database constraints are properly enforced.
    """
    app.dependency_overrides[get_current_user] = mock_get_current_user

    try:
        # Create a todo
        create_response = client.post(
            "/api/v1/todos",
            json={
                "title": "Database Consistency Test",
                "description": "Testing database constraints",
                "is_completed": False
            }
        )
        assert create_response.status_code == 201
        created_todo = create_response.json()
        todo_id = created_todo["id"]

        # Verify it exists in the database directly
        with Session(engine) as session:
            statement = select(Todo).where(Todo.id == todo_id)
            db_todo = session.exec(statement).first()
            assert db_todo is not None
            assert db_todo.title == "Database Consistency Test"
            assert db_todo.owner_id == 1  # From mock user
            assert db_todo.id == todo_id

        # Update the todo via API
        update_response = client.put(
            f"/api/v1/todos/{todo_id}",
            json={
                "title": "Updated Database Consistency Test",
                "is_completed": True
            }
        )
        assert update_response.status_code == 200

        # Verify the update happened in the database
        with Session(engine) as session:
            statement = select(Todo).where(Todo.id == todo_id)
            updated_db_todo = session.exec(statement).first()
            assert updated_db_todo is not None
            assert updated_db_todo.title == "Updated Database Consistency Test"
            assert updated_db_todo.is_completed is True

        # Delete the todo via API
        delete_response = client.delete(f"/api/v1/todos/{todo_id}")
        assert delete_response.status_code == 204

        # Verify it's gone from the database
        with Session(engine) as session:
            statement = select(Todo).where(Todo.id == todo_id)
            deleted_db_todo = session.exec(statement).first()
            assert deleted_db_todo is None

    finally:
        app.dependency_overrides.pop(get_current_user, None)


if __name__ == "__main__":
    pytest.main([__file__])