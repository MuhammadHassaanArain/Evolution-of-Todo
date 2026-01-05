from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from .base import BaseUUIDModel
from .user import User
from .user import UserRead
from datetime import datetime


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)


class Task(TaskBase, BaseUUIDModel, table=True):
    """
    Task model representing a user's task with CRUD operations
    """
    __tablename__ = "tasks"

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    user_id: str = Field(foreign_key="users.id", nullable=False)

    # Relationship to User
    user: User = Relationship(back_populates="tasks")

    # Automatically updated when the record is modified
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """
    Schema for creating a new task
    """
    title: str


class TaskUpdate(SQLModel):
    """
    Schema for updating an existing task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None


class TaskRead(TaskBase):
    """
    Schema for reading task data
    """
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime


class TaskReadWithUser(TaskRead):
    """
    Schema for reading task data with user information
    """
    user: Optional[UserRead] = None



