from fastapi.testclient import TestClient
from src.main import app
from src.models.user import UserCreate
from src.services.auth_service import auth_service
from src.database.session import get_session
from sqlmodel import Session


def test_login_with_valid_credentials():
    """
    Test login flow with valid credentials
    """
    with TestClient(app) as client:
        # First, register a user
        registration_data = {
            "email": "login_test@example.com",
            "password": "TestPassword123!",
            "first_name": "Login",
            "last_name": "Test"
        }

        # Register the user first
        register_response = client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 201

        # Now try to log in with the same credentials
        login_data = {
            "email": "login_test@example.com",
            "password": "TestPassword123!"
        }

        login_response = client.post("/auth/login", json=login_data)

        # Assert successful login
        assert login_response.status_code == 200

        # Check response structure
        data = login_response.json()
        assert "access_token" in data
        assert "token_type" in data
        assert "user" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "login_test@example.com"
        assert data["user"]["first_name"] == "Login"
        assert data["user"]["last_name"] == "Test"


if __name__ == "__main__":
    test_login_with_valid_credentials()
    print("✅ Login test with valid credentials passed")