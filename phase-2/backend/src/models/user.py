from sqlmodel import SQLModel, Field, Relationship, create_engine
from sqlalchemy import Column, String, Index
from typing import List, Optional
from datetime import datetime
from pydantic import validator
from .base import TimestampMixin
import re


class UserBase(SQLModel):
    """
    Base model for User with common fields.
    """
    email: str = Field(unique=True, nullable=False, max_length=255, sa_column=Column("email", String, unique=True, nullable=False))
    username: str = Field(unique=True, nullable=False, max_length=50, sa_column=Column("username", String, unique=True, nullable=False))
    first_name: Optional[str] = Field(default=None, max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, TimestampMixin, table=True):
    """
    User model representing an authenticated account.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    
    # Relationship to Todo entities
    todos: List["Todo"] = Relationship(back_populates="owner")
    
    @validator("email")
    def validate_email(cls, v):
        """
        Validate email format.
        """
        if not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")
        return v
    
    @validator("username")
    def validate_username(cls, v):
        """
        Validate username format (alphanumeric and underscores only).
        """
        if not re.match(r"^[a-zA-Z0-9_]{3,50}$", v):
            raise ValueError("Username must be 3-50 characters long and contain only letters, numbers, and underscores")
        return v


class UserCreate(UserBase):
    """
    Model for creating a new user.
    """
    password: str
    
    @validator("password")
    def validate_password(cls, v):
        """
        Validate password strength.
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserUpdate(SQLModel):
    """
    Model for updating user information.
    """
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None
    
    @validator("email")
    def validate_email(cls, v):
        """
        Validate email format if provided.
        """
        if v and not re.match(r"[^@]+@[^@]+\.[^@]+", v):
            raise ValueError("Invalid email format")
        return v


class UserRead(UserBase):
    """
    Model for reading user information (without sensitive data).
    """
    id: int
    created_at: datetime
    updated_at: datetime
