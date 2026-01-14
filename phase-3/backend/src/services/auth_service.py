from datetime import datetime, timedelta
from typing import Optional
from sqlmodel import Session, select
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from src.config.settings import settings
from ..models.user import User, UserCreate
from ..utils.logging import log_auth_event


class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
        self.secret_key = settings.jwt_secret
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire_minutes = settings.jwt_expiration_minutes

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password
        """
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        """
        Generate a hash for the given password
        """
        return self.pwd_context.hash(password)

    def authenticate_user(self, session: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user by email and password
        """
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()

        if not user or not self.verify_password(password, user.hashed_password):
            log_auth_event("login_failed", user=user, success=False, details={"reason": "invalid_credentials"})
            return None

        log_auth_event("login_success", user=user, success=True)
        return user

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a new access token
        """
        to_encode = data.copy()

        # Ensure sub is always a string for consistent JWT handling
        if "sub" in to_encode:
            to_encode["sub"] = str(to_encode["sub"])

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> Optional[dict]:
        """
        Decode a token and return the payload
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

    def get_current_user(self, session: Session, token: str) -> Optional[User]:
        """
        Get the current user from the token
        """
        payload = self.decode_token(token)
        if payload is None:
            return None

        # Extract sub from payload and convert to int for database lookup
        user_id_str = payload.get("sub")
        if user_id_str is None:
            return None

        # Convert string sub back to integer for database query
        try:
            user_id: int = int(user_id_str)
        except (ValueError, TypeError):
            return None

        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        return user

    def create_user(self, session: Session, user_create: UserCreate) -> User:
        """
        Create a new user with the provided data
        """
        # Check if user already exists
        statement = select(User).where(User.email == user_create.email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise ValueError("Email already registered")

        # Hash the password
        hashed_password = self.get_password_hash(user_create.password)

        # Validate that username is provided
        if not user_create.username or not user_create.username.strip():
            raise ValueError("Username is required and cannot be empty")

        # Create new user
        user = User(
            email=user_create.email,
            username=user_create.username,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            hashed_password=hashed_password,
            is_active=True,
            email_verified=False
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        log_auth_event("registration_success", user=user, success=True)
        return user


# Create a singleton instance of the AuthService
auth_service = AuthService()