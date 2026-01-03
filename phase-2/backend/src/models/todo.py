from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Integer, DateTime
from typing import Optional
from datetime import datetime
from .base import TimestampMixin
from .user import User


class TodoBase(SQLModel):
    """
    Base model for Todo with common fields.
    """
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)
    due_date: Optional[datetime] = Field(default=None)


class Todo(TodoBase, TimestampMixin, table=True):
    """
    Todo model representing a task owned by a user.
    """
    id: Optional[int] = Field(default=None, primary_key=True)

    # Foreign key to User with non-nullable constraint and indexing for user-scoped queries
    owner_id: int = Field(
        sa_column=Column("owner_id", Integer, nullable=False, index=True, foreign_key="user.id", ondelete="CASCADE")
    )

    # Relationship to User entity
    owner: User = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    """
    Model for creating a new todo.
    """
    owner_id: int
    
    def __init__(self, **data):
        super().__init__(**data)
        # Ensure title is not empty
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")


class TodoUpdate(SQLModel):
    """
    Model for updating todo information.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None
    due_date: Optional[datetime] = None


class TodoRead(TodoBase):
    """
    Model for reading todo information.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
