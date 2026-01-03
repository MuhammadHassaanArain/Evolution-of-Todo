import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from src.main import app
from src.models.user import User
from src.database.session import engine


def test_registration_with_valid_credentials():
    """
    Test registration flow with valid credentials
    """
    with TestClient(app) as client:
        # Prepare valid registration data
        registration_data = {
            "email": "test@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }

        # Make registration request
        response = client.post("/auth/register", json=registration_data)

        # Assert successful registration
        assert response.status_code == 201

        # Check response structure
        data = response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "user" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "test@example.com"
        assert data["user"]["first_name"] == "Test"
        assert data["user"]["last_name"] == "User"

        # Verify user was created in the database
        with Session(engine) as session:
            statement = select(User).where(User.email == "test@example.com")
            user = session.exec(statement).first()
            assert user is not None
            assert user.email == "test@example.com"
            assert user.first_name == "Test"
            assert user.last_name == "User"
            assert user.is_active is True
            assert user.email_verified is False


if __name__ == "__main__":
    test_registration_with_valid_credentials()
    print("✅ Registration test with valid credentials passed")