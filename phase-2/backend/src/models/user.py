from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from .base import TimestampMixin


class UserBase(SQLModel):
    """
    Base model for User with common fields.
    """
    email: str = Field(unique=True, nullable=False, max_length=255)
    username: str = Field(unique=True, nullable=False, max_length=50)
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


class UserCreate(UserBase):
    """
    Model for creating a new user.
    """
    password: str


class UserUpdate(SQLModel):
    """
    Model for updating user information.
    """
    email: Optional[str] = None
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: Optional[bool] = None


class UserRead(UserBase):
    """
    Model for reading user information (without sensitive data).
    """
    id: int
    created_at: datetime
    updated_at: datetime
