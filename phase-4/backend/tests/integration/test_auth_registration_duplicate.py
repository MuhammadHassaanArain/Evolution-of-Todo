import pytest
from fastapi.testclient import TestClient
from src.main import app


def test_registration_with_duplicate_email():
    """
    Test registration flow with duplicate email (should fail)
    """
    with TestClient(app) as client:
        # First, register a user
        first_registration_data = {
            "email": "duplicate@example.com",
            "password": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }

        # Make first registration request
        first_response = client.post("/auth/register", json=first_registration_data)

        # Assert first registration was successful
        assert first_response.status_code == 201

        # Now try to register with the same email
        duplicate_registration_data = {
            "email": "duplicate@example.com",  # Same email as before
            "password": "AnotherPassword123!",
            "first_name": "Another",
            "last_name": "User"
        }

        # Make second registration request with same email
        second_response = client.post("/auth/register", json=duplicate_registration_data)

        # Assert registration failed due to duplicate email
        assert second_response.status_code == 400

        # Check error response
        error_data = second_response.json()
        assert "detail" in error_data
        assert "already registered" in error_data["detail"].lower()


if __name__ == "__main__":
    test_registration_with_duplicate_email()
    print("✅ Registration test with duplicate email failed as expected")