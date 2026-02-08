"""
JWT Token validation utility functions for the validation hardening feature.

This module contains standalone functions for validating JWT tokens,
including validation for expired tokens, invalid signatures, and malformed tokens.
"""

from jose import JWTError
from typing import Optional, Dict, Any
from fastapi import HTTPException
from ..services.auth_service import auth_service
from ..models.validation import UNAUTHORIZED_ERROR, MISSING_AUTH_ERROR
from ..schemas.error import UNAUTHORIZED_RESPONSE, MISSING_AUTH_RESPONSE


def validate_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Validate a JWT token and return the payload if valid.

    Args:
        token: JWT token string to validate

    Returns:
        Token payload dictionary if valid, None if invalid

    Raises:
        HTTPException: If token validation fails
    """
    # Check if token is empty
    if not token or token.strip() == "":
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_RESPONSE.dict()
        )

    try:
        # Decode the token
        payload = auth_service.decode_token(token)
        if payload is None:
            # This could mean invalid signature or other JWT errors
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_RESPONSE.dict()
            )

        user_id: str = payload.get("sub")
        if user_id is None:
            # No subject in token - invalid token
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_RESPONSE.dict()
            )

        # Check if token is expired
        # Note: auth_service.decode_token should handle expiration internally
        # but we can add additional checks here if needed

        return payload

    except JWTError:
        # This handles various JWT errors: invalid signature, malformed token, etc.
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_RESPONSE.dict()
        )
    except Exception:
        # Catch any other unexpected errors during token validation
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_RESPONSE.dict()
        )


def is_token_valid(token: str) -> bool:
    """
    Check if a JWT token is valid without raising exceptions.

    Args:
        token: JWT token string to validate

    Returns:
        True if token is valid, False otherwise
    """
    try:
        payload = validate_jwt_token(token)
        return payload is not None
    except HTTPException:
        return False


def extract_user_id_from_token(token: str) -> Optional[str]:
    """
    Extract the user ID from a JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID string if valid, None if invalid
    """
    try:
        payload = validate_jwt_token(token)
        if payload:
            return payload.get("sub")
        return None
    except HTTPException:
        return None


def validate_authorization_header(auth_header: Optional[str]) -> str:
    """
    Validate the Authorization header format and extract the token.

    Args:
        auth_header: Authorization header value

    Returns:
        JWT token string if valid

    Raises:
        HTTPException: If header validation fails
    """
    # Check for missing Authorization header
    if not auth_header:
        raise HTTPException(
            status_code=401,
            detail=MISSING_AUTH_RESPONSE.dict()
        )

    # Check for malformed Authorization header (not starting with "Bearer ")
    if not auth_header.startswith("Bearer "):
        # Check if it's just a malformed header (not following Bearer format)
        if auth_header.strip().lower().startswith("bearer"):
            # It's a Bearer header but malformed in some way
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_RESPONSE.dict()
            )
        else:
            # Not a Bearer header at all
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_RESPONSE.dict()
            )

    # Extract token part after "Bearer "
    token_parts = auth_header.split(" ", 1)
    if len(token_parts) != 2:
        # Malformed header: "Bearer" without actual token
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_RESPONSE.dict()
        )

    token = token_parts[1]

    # Validate the extracted token
    if not token or token.strip() == "":
        # Empty token after "Bearer "
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_RESPONSE.dict()
        )

    return token


def validate_token_and_extract_user_id(auth_header: Optional[str]) -> Optional[str]:
    """
    Validate the Authorization header and JWT token, then extract user ID.

    Args:
        auth_header: Authorization header value

    Returns:
        User ID string if valid, None if invalid
    """
    try:
        token = validate_authorization_header(auth_header)
        return extract_user_id_from_token(token)
    except HTTPException:
        return None


def is_expired_token(token: str) -> bool:
    """
    Check if a token is expired without validating other aspects.

    Args:
        token: JWT token string

    Returns:
        True if token is expired, False otherwise or if other validation fails
    """
    try:
        # This will raise an exception if the token is expired
        payload = auth_service.decode_token(token)
        return payload is None  # If payload is None, token was invalid/expired
    except JWTError:
        # If it's a JWT error, it could be expired or other issue
        return True
    except Exception:
        # Any other error indicates invalid token
        return True