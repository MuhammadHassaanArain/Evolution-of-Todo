from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from .base import TimestampMixin
from pydantic import field_validator


class TodoBase(SQLModel):
    """
    Base model for Todo with common fields.
    """
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)

    @field_validator('title')
    def validate_title(cls, v):
        """
        Validate that the title is not empty and within length limits.
        """
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 255:
            raise ValueError('Title must be less than 255 characters')
        return v.strip()

    @field_validator('description')
    def validate_description(cls, v):
        """
        Validate that the description is within length limits if provided.
        """
        if v and len(v) > 1000:
            raise ValueError('Description must be less than 1000 characters')
        return v


class TodoUpdate(SQLModel):
    """
    Model for updating Todo information.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = Field(default=None)

    @field_validator('title')
    def validate_title(cls, v):
        """
        Validate the title during updates.
        """
        if v is not None:  # Only validate if the field is being updated
            if not v or len(v.strip()) == 0:
                raise ValueError('Title cannot be empty')
            if len(v) > 255:
                raise ValueError('Title must be less than 255 characters')
            return v.strip()
        return v

    @field_validator('description')
    def validate_description_update(cls, v):
        """
        Validate the description during updates.
        """
        if v is not None:  # Only validate if the field is being updated
            if len(v) > 1000:
                raise ValueError('Description must be less than 1000 characters')
        return v


class Todo(TodoBase, TimestampMixin, table=True):
    """
    Todo model representing a task owned by a user.
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign key to User with non-nullable constraint
    owner_id: int = Field(nullable=False, foreign_key="user.id", ondelete="CASCADE")
    
    # Relationship to User entity
    owner: "User" = Relationship(back_populates="todos")


class TodoCreate(TodoBase):
    """
    Model for creating a new todo.
    """
    pass  # All fields inherited from TodoBase


class TodoUpdate(SQLModel):
    """
    Model for updating todo information.
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: Optional[bool] = Field(default=None)


class TodoRead(TodoBase):
    """
    Model for reading todo information.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
