from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session
from ..database.session import get_session
from ..models.user import UserRead
from ..services.auth_service import auth_service
from ..services.user_service import user_service


security = HTTPBearer(
    scheme_name="JWT",
    description="JWT Bearer token for authentication",
    auto_error=True
)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> UserRead:
    """
    Get the current authenticated user from the JWT token.

    This function extracts the JWT token from the Authorization header,
    validates it, decodes the user information, and returns the user data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Extract token from credentials
        token = credentials.credentials

        # Decode the JWT token
        payload = auth_service.decode_token(token)
        if payload is None:
            raise credentials_exception

        # Extract sub from payload and convert to int for database lookup
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        # Convert string sub back to integer for database query
        try:
            user_id: int = int(user_id_str)
        except (ValueError, TypeError):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    try:
        # Fetch user from database
        user = user_service.get_user_by_id(session, user_id)
        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Inactive user",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Convert to UserRead schema for API responses
        return UserRead(
            id=user.id,
            email=user.email,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    except NoResultFound:
        raise credentials_exception
    except Exception as e:
        raise credentials_exception


# Alternative function for optional authentication (doesn't raise error if not authenticated)
async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
) -> UserRead:
    """
    Get the current authenticated user if authenticated, otherwise return None.
    """
    try:
        return await get_current_user(credentials, session)
    except HTTPException:
        return None