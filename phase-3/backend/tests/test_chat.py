"""
Tests for the chat functionality
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from backend.main import app  # Assuming the main FastAPI app is in main.py
from backend.database import get_session


# Create a test database engine
@pytest.fixture(name="engine")
def engine_fixture():
    engine = create_engine("sqlite:///./test.db", echo=True)
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()


@pytest.fixture(name="session")
def session_fixture(engine):
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session):
    def get_test_session():
        return session

    app.dependency_overrides[get_session] = get_test_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_chat_endpoint_exists(client: TestClient):
    """
    Test that the chat endpoint is available
    """
    # This is a basic test to check if the endpoint exists
    # Since we can't easily test the AI functionality without mocking,
    # we'll focus on the API structure

    # Mock request without a real token
    response = client.post("/api/chat", json={"message": "test"})

    # Expect 401 Unauthorized since no token provided
    assert response.status_code in [401, 422]  # 401 for auth failure, 422 for validation error


def test_conversations_endpoint_exists(client: TestClient):
    """
    Test that the conversations endpoint is available
    """
    response = client.get("/api/conversations")

    # Expect 401 Unauthorized since no token provided
    assert response.status_code == 401


def test_conversation_messages_endpoint_exists(client: TestClient):
    """
    Test that the conversation messages endpoint is available
    """
    response = client.get("/api/conversations/1/messages")

    # Expect 401 Unauthorized since no token provided
    assert response.status_code == 401