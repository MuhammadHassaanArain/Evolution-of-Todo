from sqlmodel import Field, SQLModel
from typing import Optional
from .base import BaseUUIDModel
from datetime import datetime
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)


class User(UserBase, BaseUUIDModel, table=True):
    """
    User model representing an authenticated user in the system
    """
    __tablename__ = "users"

    email: str = Field(unique=True, nullable=False, max_length=255)
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    email_verified: bool = Field(default=False)

    # Automatically updated when the record is modified
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """
    Schema for creating a new user
    """
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserUpdate(SQLModel):
    """
    Schema for updating an existing user
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information)
    """
    id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: str
    is_active: bool
    email_verified: bool
    created_at: datetime
    updated_at: datetime


class UserLogin(SQLModel):
    """
    Schema for user login
    """
    email: str
    password: str


class UserWithPassword(UserRead):
    """
    Schema for reading user data with password (for internal use)
    """
    hashed_password: str