# from sqlmodel import Field, SQLModel, Relationship
# from typing import Optional, TYPE_CHECKING
# from .base import BaseUUIDModel
# from .user import User
# from .user import UserRead
# from datetime import datetime


# class TaskBase(SQLModel):
#     title: str = Field(min_length=1, max_length=200)
#     description: Optional[str] = Field(default=None, max_length=1000)
#     is_completed: bool = Field(default=False)

# if TYPE_CHECKING:
#     from .user import User

# class Task(TaskBase, BaseUUIDModel, table=True):
#     __tablename__ = "tasks"

#     user_id: int = Field(foreign_key="users.id", nullable=False)  # must match User.id type

#     # Relationship to User
#     user: Optional["User"] = Relationship(back_populates="tasks")

#     updated_at: datetime = Field(default_factory=datetime.utcnow)

# class TaskCreate(TaskBase):
#     """
#     Schema for creating a new task
#     """
#     title: str


# class TaskUpdate(SQLModel):
#     """
#     Schema for updating an existing task
#     """
#     title: Optional[str] = None
#     description: Optional[str] = None
#     is_completed: Optional[bool] = None


# class TaskRead(TaskBase):
#     """
#     Schema for reading task data
#     """
#     id: str
#     user_id: str
#     created_at: datetime
#     updated_at: datetime


# class TaskReadWithUser(TaskRead):
#     """
#     Schema for reading task data with user information
#     """
#     user: Optional[UserRead] = None

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from .base import BaseUUIDModel

if TYPE_CHECKING:
    from .user import User, UserRead

class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = Field(default=False)

from .base import TimestampMixin

class Task(TaskBase, BaseUUIDModel, table=True):
    __tablename__ = "tasks"

    user_id: int = Field(foreign_key="users.id", nullable=False)  # must match User.__tablename__

    # Add timestamps directly to match the TaskRead schema expectations
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to User (using string reference to avoid circular import)
    user: Optional["User"] = Relationship(back_populates="tasks")

# Schemas
class TaskCreate(TaskBase):
    title: str

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskRead(TaskBase):
    id: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Enable ORM mode for SQLModel compatibility

class TaskReadWithUser(TaskRead):
    user: Optional["UserRead"] = None
