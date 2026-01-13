from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TodoBase(BaseModel):
    """
    Base schema for Todo model with shared attributes.
    """
    title: str = Field(..., min_length=1, max_length=255, description="Title of the todo item")
    description: Optional[str] = Field(None, max_length=1000, description="Optional description of the todo")
    is_completed: bool = Field(False, description="Whether the todo is completed")


class TodoCreate(TodoBase):
    """
    Schema for creating a new Todo.
    """
    # Inherits all fields from TodoBase
    pass


class TodoUpdate(BaseModel):
    """
    Schema for updating an existing Todo.
    """
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Updated title of the todo item")
    description: Optional[str] = Field(None, max_length=1000, description="Updated description of the todo")
    is_completed: Optional[bool] = Field(None, description="Updated completion status")


class TodoResponse(TodoBase):
    """
    Schema for returning Todo data to the client.
    """
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TodoListResponse(BaseModel):
    """
    Schema for returning a list of Todo items.
    """
    todos: list[TodoResponse]
    total_count: int


class TodoOwnershipCheck(BaseModel):
    """
    Schema for checking ownership of a Todo.
    """
    user_id: int
    todo_id: int
    has_permission: bool
    detail: str
