from fastapi.testclient import TestClient
from src.main import app


def test_auth_me_with_valid_token():
    """
    Test /auth/me endpoint with valid JWT token
    """
    with TestClient(app) as client:
        # First, register a user
        registration_data = {
            "email": "me_test@example.com",
            "password": "TestPassword123!",
            "first_name": "Me",
            "last_name": "Test"
        }

        register_response = client.post("/auth/register", json=registration_data)
        assert register_response.status_code == 201

        # Extract the token from the registration response
        register_data = register_response.json()
        token = register_data["access_token"]

        # Make request to /auth/me with the token
        me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})

        # Assert successful response
        assert me_response.status_code == 200

        # Check response structure
        me_data = me_response.json()
        assert "id" in me_data
        assert "email" in me_data
        assert "first_name" in me_data
        assert "last_name" in me_data
        assert "is_active" in me_data
        assert "email_verified" in me_data
        assert me_data["email"] == "me_test@example.com"
        assert me_data["first_name"] == "Me"
        assert me_data["last_name"] == "Test"


if __name__ == "__main__":
    test_auth_me_with_valid_token()
    print("✅ /auth/me test with valid token passed")