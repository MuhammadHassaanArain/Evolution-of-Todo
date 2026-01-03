from fastapi.testclient import TestClient
from src.main import app


def test_logout_functionality():
    """
    Test logout functionality
    Note: In a stateless JWT system, logout is primarily handled on the client side
    This test verifies that the logout endpoint exists and returns the expected response
    """
    with TestClient(app) as client:
        # First, register and login a user to get a token
        registration_data = {
            "email": "logout_test@example.com",
            "password": "TestPassword123!",
            "first_name": "Logout",
            "last_name": "Test"
        }

        register_response = client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 201

        login_data = {
            "email": "logout_test@example.com",
            "password": "TestPassword123!"
        }

        login_response = client.post("/auth/login", json=login_data)
        assert login_response.status_code == 200

        login_data_response = login_response.json()
        token = login_data_response["access_token"]

        # Verify that we can access /auth/me with the token
        me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_response.status_code == 200

        # Call the logout endpoint
        logout_response = client.post("/auth/logout", headers={"Authorization": f"Bearer {token}"})
        assert logout_response.status_code == 200

        # In a stateless JWT system, the token is still valid until expiration
        # The server doesn't maintain session state
        # However, the client should clear the token locally
        logout_data = logout_response.json()
        assert "message" in logout_data
        assert logout_data["message"] == "Successfully logged out"

        # Note: The token would still technically work until expiration
        # since JWTs are stateless, but the client should clear it


if __name__ == "__main__":
    test_logout_functionality()
    print("✅ Logout test completed")