from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from .user import UserRead


class Token(BaseModel):
    """
    Token response model
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Token data model for internal use
    """
    user_id: Optional[str] = None
    email: Optional[str] = None


class AuthResponse(BaseModel):
    """
    Authentication response model
    """
    access_token: str
    token_type: str
    user: UserRead


class UserLogin(BaseModel):
    """
    User login request model
    """
    email: str
    password: str


class UserRegister(BaseModel):
    """
    User registration request model
    """
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class AuthMeResponse(BaseModel):
    """
    Authentication me response model
    """
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime
    is_active: bool
    email_verified: bool


class AuthSuccessResponse(BaseModel):
    """
    Authentication success response model
    """
    success: bool
    message: str
    data: Token


class AuthErrorResponse(BaseModel):
    """
    Authentication error response model
    """
    success: bool
    message: str
    error_code: str