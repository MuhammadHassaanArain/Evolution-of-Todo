from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime
from .base import TimestampMixin
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .task import Task

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
    todos: List["Task"] = Relationship(back_populates="user")


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


class UserLogin(SQLModel):
    """
    Model for user login credentials.
    """
    email: str
    password: str


class UserWithPassword(UserRead):
    """
    Model for user with password information (for internal use).
    """
    hashed_password: str
