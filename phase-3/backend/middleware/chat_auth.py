from fastapi import HTTPException, Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from typing import Optional
import os
from datetime import datetime, timedelta


class ChatAuthMiddleware:
    """
    Authentication middleware specifically for chat endpoints
    Validates JWT tokens and extracts user context
    """

    def __init__(self):
        self.secret_key = os.getenv("JWT_SECRET", "fallback_secret_for_dev")
        self.algorithm = os.getenv("JWT_ALGORITHM", "HS256")
        self.security = HTTPBearer()

    async def authenticate_request(self, request: Request) -> Optional[str]:
        """
        Authenticate the request and return the user_id if valid
        """
        try:
            # Get the authorization header
            auth_header = request.headers.get("authorization")
            if not auth_header:
                raise HTTPException(status_code=401, detail="Authorization header missing")

            # Extract the token (format: "Bearer <token>")
            if not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Invalid authorization header format")

            token = auth_header[len("Bearer "):]

            # Decode and verify the JWT token
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])

            # Extract user_id from the token
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: no user ID")

            # Check if token is expired
            exp_time = payload.get("exp")
            if exp_time and datetime.fromtimestamp(exp_time) < datetime.utcnow():
                raise HTTPException(status_code=401, detail="Token expired")

            return user_id

        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


# Global instance for use in routes
chat_auth = ChatAuthMiddleware()