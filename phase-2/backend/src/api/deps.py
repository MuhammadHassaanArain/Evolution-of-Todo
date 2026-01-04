from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Generator
from sqlmodel import Session
from ..database.connection import get_session
from ..utils.jwt import verify_access_token, get_user_id_from_token
from ..models.user import User
from ..models.validation import UNAUTHORIZED_ERROR, MISSING_AUTH_ERROR
from ..schemas.error import UNAUTHORIZED_RESPONSE, MISSING_AUTH_RESPONSE
from ..utils.jwt_validator import validate_authorization_header, validate_jwt_token


# Initialize the HTTP Bearer security scheme
security = HTTPBearer(
    scheme_name="JWT Authentication",
    description="Provide a valid JWT token in the Authorization header",
    auto_error=True
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user from the JWT token with enhanced validation.

    Args:
        credentials: The HTTP authorization credentials from the request header
        session: Database session for querying user data

    Returns:
        The authenticated User object

    Raises:
        HTTPException: If the token is invalid, expired, or the user doesn't exist
    """
    token = credentials.credentials

    # Validate the JWT token using the enhanced validation
    payload = validate_jwt_token(token)

    # Get the user ID from the token
    user_id = payload.get("sub") if payload else None
    if not user_id:
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_RESPONSE.dict()
        )

    # Query the database for the user
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_RESPONSE.dict()
        )

    # Check if the user is active
    if not user.is_active:
        raise HTTPException(
            status_code=401,
            detail=UNAUTHORIZED_RESPONSE.dict()
        )

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """
    Dependency to get the current active user.

    Args:
        current_user: The current authenticated user (from get_current_user)

    Returns:
        The authenticated User object (verified to be active)

    Raises:
        HTTPException: If the user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user


def get_optional_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current user, but doesn't raise an exception if authentication fails.
    This is useful for endpoints that can be accessed by both authenticated and unauthenticated users.

    Args:
        credentials: The HTTP authorization credentials from the request header
        session: Database session for querying user data

    Returns:
        The authenticated User object, or None if authentication fails
    """
    try:
        token = credentials.credentials

        # Validate the JWT token using the enhanced validation
        payload = validate_jwt_token(token)
        if not payload:
            return None

        # Get the user ID from the token
        user_id = payload.get("sub")
        if not user_id:
            return None

        # Query the database for the user
        user = session.get(User, user_id)
        if not user or not user.is_active:
            return None

        return user
    except HTTPException:
        # If it's an HTTPException (like validation errors), return None
        return None
    except Exception:
        # If any other error occurs during authentication, return None
        return None


def require_user_ownership(
    requested_user_id: int,
    current_user: User = Depends(get_current_user)
) -> bool:
    """
    Dependency to ensure that the current user owns the requested resource.

    Args:
        requested_user_id: The ID of the user/resource being accessed
        current_user: The current authenticated user

    Returns:
        True if the current user owns the requested resource

    Raises:
        HTTPException: If the current user doesn't own the requested resource
    """
    if current_user.id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Insufficient permissions"
        )
    return True


def get_db_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session.

    Yields:
        Database session for use in API endpoints
    """
    yield from get_session()
