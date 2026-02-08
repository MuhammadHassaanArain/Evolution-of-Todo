from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from fastapi import HTTPException, status
from ..config.auth import SECRET_KEY, ALGORITHM, auth_settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create an access token with the provided data.

    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration (uses default if not provided)

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + auth_settings.get_access_token_expires_delta()

    to_encode.update({"exp": expire, "type": "access"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a refresh token with the provided data.

    Args:
        data: Dictionary containing the data to encode in the token
        expires_delta: Optional timedelta for token expiration (uses default if not provided)

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + auth_settings.get_refresh_token_expires_delta()

    to_encode.update({"exp": expire, "type": "refresh"})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify the JWT token and return the decoded payload if valid.

    Args:
        token: JWT token string to verify

    Returns:
        Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.JWTError:
        # Invalid token
        return None
    except Exception:
        # Other error occurred
        return None


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode the JWT token without verification (use with caution).

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload if successful, None otherwise
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        return payload
    except Exception:
        return None


def get_user_id_from_token(token: str) -> Optional[int]:
    """
    Extract user ID from the JWT token.

    Args:
        token: JWT token string

    Returns:
        User ID if found and valid, None otherwise
    """
    payload = verify_token(token)
    if payload:
        user_id = payload.get("sub")
        if user_id:
            # Ensure it's an integer
            try:
                return int(user_id)
            except (ValueError, TypeError):
                return None
    return None


def get_token_type(token: str) -> Optional[str]:
    """
    Get the type of the token (access or refresh).

    Args:
        token: JWT token string

    Returns:
        Token type if found, None otherwise
    """
    payload = verify_token(token)
    if payload:
        return payload.get("type")
    return None


def is_token_expired(token: str) -> bool:
    """
    Check if the token is expired.

    Args:
        token: JWT token string

    Returns:
        True if expired, False otherwise
    """
    payload = verify_token(token)
    if payload is None:
        # Token is either expired or invalid
        return True

    exp = payload.get("exp")
    if exp:
        return datetime.utcnow() > datetime.utcfromtimestamp(exp)
    return False


def validate_token_for_user(token: str, expected_user_id: int) -> bool:
    """
    Validate that the token belongs to the expected user.

    Args:
        token: JWT token string
        expected_user_id: Expected user ID

    Returns:
        True if token is valid and belongs to the expected user, False otherwise
    """
    token_user_id = get_user_id_from_token(token)
    return token_user_id == expected_user_id


def create_token_payload(user_id: int, additional_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Create a standard token payload with user ID and additional data.

    Args:
        user_id: User ID to include in the token
        additional_data: Additional data to include in the token

    Returns:
        Dictionary with token payload
    """
    payload = {"sub": str(user_id)}

    if additional_data:
        payload.update(additional_data)

    return payload


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify that the token is an access token and is valid.

    Args:
        token: JWT token string

    Returns:
        Payload if valid access token, None otherwise
    """
    payload = verify_token(token)
    if payload and payload.get("type") == "access":
        return payload
    return None


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify that the token is a refresh token and is valid.

    Args:
        token: JWT token string

    Returns:
        Payload if valid refresh token, None otherwise
    """
    payload = verify_token(token)
    if payload and payload.get("type") == "refresh":
        return payload
    return None


def require_access_token(token: str) -> Dict[str, Any]:
    """
    Require a valid access token, raising an exception if invalid.

    Args:
        token: JWT token string

    Returns:
        Token payload if valid

    Raises:
        HTTPException: If token is invalid or not an access token
    """
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def require_refresh_token(token: str) -> Dict[str, Any]:
    """
    Require a valid refresh token, raising an exception if invalid.

    Args:
        token: JWT token string

    Returns:
        Token payload if valid

    Raises:
        HTTPException: If token is invalid or not a refresh token
    """
    payload = verify_refresh_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload
