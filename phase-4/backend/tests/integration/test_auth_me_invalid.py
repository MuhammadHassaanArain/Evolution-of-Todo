from fastapi.testclient import TestClient
from src.main import app


def test_auth_me_with_invalid_token():
    """
    Test /auth/me endpoint with invalid JWT token (should return 401)
    """
    with TestClient(app) as client:
        # Make request to /auth/me with an invalid token
        invalid_token = "invalid.token.here"

        me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {invalid_token}"})

        # Assert unauthorized response
        assert me_response.status_code == 401

        # Check error response
        error_data = me_response.json()
        assert "detail" in error_data


def test_auth_me_with_expired_token():
    """
    Test /auth/me endpoint with expired JWT token (should return 401)
    For this test, we'll use a properly formatted but expired token
    """
    with TestClient(app) as client:
        # This is a JWT with an expired time (past date)
        # Header: {"alg": "HS256", "typ": "JWT"}
        # Payload: {"sub": "test_user", "exp": 1234567890} (past date)
        # Signature: dummy signature
        expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXIiLCJleHAiOjEyMzQ1Njc4OTB9.dummy_signature"

        me_response = client.get("/auth/me", headers={"Authorization": f"Bearer {expired_token}"})

        # Assert unauthorized response
        assert me_response.status_code == 401

        # Check error response
        error_data = me_response.json()
        assert "detail" in error_data


def test_auth_me_without_token():
    """
    Test /auth/me endpoint without any token (should return 401)
    """
    with TestClient(app) as client:
        # Make request to /auth/me without any token
        me_response = client.get("/auth/me")

        # Assert unauthorized response
        assert me_response.status_code == 401

        # Check error response
        error_data = me_response.json()
        assert "detail" in error_data


if __name__ == "__main__":
    test_auth_me_with_invalid_token()
    test_auth_me_with_expired_token()
    test_auth_me_without_token()
    print("✅ /auth/me tests with invalid/expired tokens returned 401 as expected")