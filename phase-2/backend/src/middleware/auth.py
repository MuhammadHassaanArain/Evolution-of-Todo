from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from ..services.auth_service import auth_service
from ..services.user_service import user_service
from ..models.user import User
from sqlmodel import Session
from ..database.session import get_session


class AuthMiddleware:
    def __init__(self):
        self.security = HTTPBearer()

    async def authenticate_user_from_token(self, token: str) -> User:
        """
        Authenticate user from JWT token
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        try:
            payload = auth_service.decode_token(token)
            if payload is None:
                raise credentials_exception

            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception

        except JWTError:
            raise credentials_exception

        # Get database session
        session_gen = get_session()
        session: Session = next(session_gen)

        try:
            user = user_service.get_user_by_id(session, user_id)
            if user is None:
                raise credentials_exception
            if not user.is_active:
                raise credentials_exception
        finally:
            session.close()

        return user

    async def get_current_user(self, request: Request) -> User:
        """
        Get the current authenticated user from the request
        """
        # Extract the token from the Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header missing or invalid",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = auth_header.split(" ")[1]
        return await self.authenticate_user_from_token(token)

    async def optional_user(self, request: Request) -> User:
        """
        Get the current user if authenticated, otherwise return None
        """
        try:
            return await self.get_current_user(request)
        except HTTPException:
            return None


# Create a singleton instance of the AuthMiddleware
auth_middleware = AuthMiddleware()