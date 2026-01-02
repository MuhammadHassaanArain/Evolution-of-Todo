"""
Unit tests for the authentication service
"""
import pytest
from unittest.mock import Mock, patch
from src.services.auth_service import AuthService


def test_verify_password():
    """Test password verification"""
    auth_service = AuthService()

    # Test that a correct password verifies
    plain_password = "testpassword"
    hashed = auth_service.get_password_hash(plain_password)
    assert auth_service.verify_password(plain_password, hashed) == True

    # Test that an incorrect password does not verify
    assert auth_service.verify_password("wrongpassword", hashed) == False


def test_create_access_token():
    """Test creating an access token"""
    auth_service = AuthService()

    data = {"sub": "testuser", "email": "test@example.com"}
    token = auth_service.create_access_token(data)

    # The token should be a string
    assert isinstance(token, str)
    assert len(token) > 0


def test_decode_token():
    """Test decoding a token"""
    auth_service = AuthService()

    data = {"sub": "testuser", "email": "test@example.com"}
    token = auth_service.create_access_token(data)

    decoded = auth_service.decode_token(token)

    # The decoded data should match the original data
    assert decoded is not None
    assert decoded["sub"] == "testuser"
    assert decoded["email"] == "test@example.com"


def test_decode_invalid_token():
    """Test decoding an invalid token"""
    auth_service = AuthService()

    decoded = auth_service.decode_token("invalid_token_string")

    # The decoded data should be None for an invalid token
    assert decoded is None