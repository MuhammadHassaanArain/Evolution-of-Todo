from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from datetime import timedelta
from ..database.session import get_session
from ..models.user import UserCreate, UserLogin, UserRead
from ..services.user_service import user_service
from ..services.auth_service import auth_service
from ..middleware.auth import auth_middleware
from ..utils.logging import log_auth_event


router = APIRouter()


@router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user
    """
    try:
        db_user = user_service.create_user(session, user)
        log_auth_event("registration_success", user=db_user, success=True)
        return UserRead.from_orm(db_user)
    except ValueError as e:
        log_auth_event("registration_failed", user=None, success=False, details={"reason": str(e)})
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/auth/login")
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Login a user and return access token
    """
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
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserRead.from_orm(user)
    }


@router.post("/auth/logout")
def logout():
    """
    Logout a user
    """
    # In a stateless JWT system, the server doesn't store sessions
    # So logout is typically handled on the client side
    # This endpoint can be used to invalidate tokens on the client
    return {"message": "Successfully logged out"}


@router.get("/auth/me", response_model=UserRead)
def get_current_user(current_user: UserRead = Depends(auth_middleware.get_current_user)):
    """
    Get current authenticated user
    """
    return current_user