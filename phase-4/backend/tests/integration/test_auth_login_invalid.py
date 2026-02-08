from fastapi.testclient import TestClient
from src.main import app


def test_login_with_invalid_credentials():
    """
    Test login flow with invalid credentials (should fail)
    """
    with TestClient(app) as client:
        # Try to log in with invalid credentials
        login_data = {
            "email": "nonexistent@example.com",
            "password": "WrongPassword123!"
        }

        login_response = client.post("/auth/login", json=login_data)

        # Assert login failed
        assert login_response.status_code == 401

        # Check error response
        error_data = login_response.json()
        assert "detail" in error_data
        assert "Incorrect email or password" in error_data["detail"]


def test_login_with_wrong_password():
    """
    Test login with correct email but wrong password
    """
    with TestClient(app) as client:
        # First, register a user
        registration_data = {
            "email": "wrong_password_test@example.com",
            "password": "CorrectPassword123!",
            "first_name": "Wrong",
            "last_name": "Password"
        }

        # Register the user first
        register_response = client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 201

        # Now try to log in with wrong password
        login_data = {
            "email": "wrong_password_test@example.com",
            "password": "WrongPassword123!"  # Different from registration
        }

        login_response = client.post("/auth/login", json=login_data)

        # Assert login failed
        assert login_response.status_code == 401

        # Check error response
        error_data = login_response.json()
        assert "detail" in error_data
        assert "Incorrect email or password" in error_data["detail"]


if __name__ == "__main__":
    test_login_with_invalid_credentials()
    test_login_with_wrong_password()
    print("✅ Login tests with invalid credentials failed as expected")