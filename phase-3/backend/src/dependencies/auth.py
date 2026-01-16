"""Authentication dependency for the chatbot backend."""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status, Request
from sqlmodel import Session
from ..database.session import get_session
from ..models.user import User  # Assuming user model exists
# from ..services.auth_service import verify_token  # Assuming auth service exists
from ..services.auth_service import auth_service
def get_current_user(
    request: Request,
    session: Session = Depends(get_session)
) -> User:
    """
    Get the current authenticated user from the request.

    Args:
        request: The incoming request with authentication header
        session: Database session

    Returns:
        The authenticated user

    Raises:
        HTTPException: If authentication fails
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = auth_header.split(" ")[1]

    try:
        user_id = auth_service.verify_password(token)
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}",
        )


CurrentUser = Depends(get_current_user)