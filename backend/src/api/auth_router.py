from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from ..database.session import get_session
from ..models.user import UserCreate, UserLogin, UserRead
from ..models.auth import AuthResponse
from ..services.auth_service import auth_service
from ..api.deps import get_current_user
from ..utils.logging import log_auth_event
from ..utils.password import validate_password_strength
import logging


router = APIRouter()


@router.post("/auth/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    try:
        # Validate password strength
        if not validate_password_strength(user.password):
            log_auth_event("registration_failed", user=None, success=False, details={"reason": "weak_password"})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password does not meet strength requirements"
            )

        db_user = auth_service.create_user(session, user)
        log_auth_event("registration_success", user=db_user, success=True)

        # Create access token
        access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
        access_token = auth_service.create_access_token(
            data={"sub": db_user.id}, expires_delta=access_token_expires
        )

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead.from_orm(db_user)
        )
    except ValueError as e:
        log_auth_event("registration_failed", user=None, success=False, details={"reason": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logging.error(f"Unexpected error during registration: {str(e)}")
        log_auth_event("registration_failed", user=None, success=False, details={"reason": "unexpected_error", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration"
        )


@router.post("/auth/login", response_model=AuthResponse)
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Login a user and return access token
    """
    try:
        user = auth_service.authenticate_user(
            session, user_credentials.email, user_credentials.password
        )
        if not user:
            log_auth_event("login_failed", user=None, success=False, details={"reason": "invalid_credentials", "email": user_credentials.email})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            log_auth_event("login_failed", user=user, success=False, details={"reason": "inactive_user"})
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
        access_token = auth_service.create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        log_auth_event("token_issued", user=user, success=True, details={"token_type": "access_token"})

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserRead.from_orm(user)
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logging.error(f"Unexpected error during login: {str(e)}")
        log_auth_event("login_failed", user=None, success=False, details={"reason": "unexpected_error", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login"
        )


@router.post("/auth/logout")
def logout():
    """
    Logout a user
    """
    try:
        # In a stateless JWT system, the server doesn't store sessions
        # So logout is typically handled on the client side
        # This endpoint can be used to invalidate tokens on the client
        log_auth_event("logout", user=None, success=True, details={"action": "logout_request"})
        return {"message": "Successfully logged out"}
    except Exception as e:
        logging.error(f"Unexpected error during logout: {str(e)}")
        log_auth_event("logout_failed", user=None, success=False, details={"reason": "unexpected_error", "error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during logout"
        )


@router.get("/auth/me", response_model=UserRead)
def get_current_user_endpoint(current_user: UserRead = Depends(get_current_user)):
    """
    Get current authenticated user
    """
    try:
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
                headers={"WWW-Authenticate": "Bearer"},
            )

        log_auth_event("get_user_success", user=current_user, success=True, details={"action": "auth_me_request"})
        return current_user
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logging.error(f"Unexpected error getting current user: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving user information"
        )