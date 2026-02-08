from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer
from jose import JWTError
from ..services.auth_service import auth_service
from ..services.user_service import user_service
from ..models.user import User
from sqlmodel import Session
from ..database.session import get_session
from ..models.validation import UNAUTHORIZED_ERROR, MISSING_AUTH_ERROR


class AuthMiddleware:
    def __init__(self):
        self.security = HTTPBearer()

    async def authenticate_user_from_token(self, token: str) -> User:
        """
        Authenticate user from JWT token with comprehensive validation.
        Handles expired tokens, invalid signatures, and malformed tokens.
        """
        # Check if token is empty
        if not token or token.strip() == "":
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_ERROR
            )

        try:
            # Decode the token
            payload = auth_service.decode_token(token)
            if payload is None:
                # This could mean invalid signature or other JWT errors
                raise HTTPException(
                    status_code=401,
                    detail=UNAUTHORIZED_ERROR
                )

            user_id: str = payload.get("sub")
            if user_id is None:
                # No subject in token - invalid token
                raise HTTPException(
                    status_code=401,
                    detail=UNAUTHORIZED_ERROR
                )

            # Check if token is expired
            # Note: auth_service.decode_token should handle expiration internally
            # but we can add additional checks here if needed

        except JWTError:
            # This handles various JWT errors: invalid signature, malformed token, etc.
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_ERROR
            )
        except Exception:
            # Catch any other unexpected errors during token validation
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_ERROR
            )

        # Get database session
        session_gen = get_session()
        session: Session = next(session_gen)

        try:
            user = user_service.get_user_by_id(session, user_id)
            if user is None:
                # User doesn't exist - invalid token
                raise HTTPException(
                    status_code=401,
                    detail=UNAUTHORIZED_ERROR
                )
            if not user.is_active:
                # User is not active - unauthorized
                raise HTTPException(
                    status_code=401,
                    detail=UNAUTHORIZED_ERROR
                )
        finally:
            session.close()

        return user

    async def get_current_user(self, request: Request) -> User:
        """
        Get the current authenticated user from the request with comprehensive validation.
        Handles missing, malformed, expired, and invalid signature tokens.
        """
        # Extract the token from the Authorization header
        auth_header = request.headers.get("Authorization")

        # Check for missing Authorization header
        if not auth_header:
            raise HTTPException(
                status_code=401,
                detail=MISSING_AUTH_ERROR
            )

        # Check for malformed Authorization header (not starting with "Bearer ")
        if not auth_header.startswith("Bearer "):
            # Check if it's just a malformed header (not following Bearer format)
            if auth_header.strip().lower().startswith("bearer"):
                # It's a Bearer header but malformed in some way
                raise HTTPException(
                    status_code=401,
                    detail=UNAUTHORIZED_ERROR
                )
            else:
                # Not a Bearer header at all
                raise HTTPException(
                    status_code=401,
                    detail=UNAUTHORIZED_ERROR
                )

        # Extract token part after "Bearer "
        token_parts = auth_header.split(" ", 1)
        if len(token_parts) != 2:
            # Malformed header: "Bearer" without actual token
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_ERROR
            )

        token = token_parts[1]

        # Validate the extracted token
        if not token or token.strip() == "":
            # Empty token after "Bearer "
            raise HTTPException(
                status_code=401,
                detail=UNAUTHORIZED_ERROR
            )

        return await self.authenticate_user_from_token(token)

    async def optional_user(self, request: Request) -> User:
        """
        Get the current user if authenticated, otherwise return None.
        This method maintains the same validation as get_current_user but returns None instead of raising exceptions.
        """
        try:
            return await self.get_current_user(request)
        except HTTPException:
            return None


# Create a singleton instance of the AuthMiddleware
auth_middleware = AuthMiddleware()