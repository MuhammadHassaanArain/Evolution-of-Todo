from sqlmodel import Session, select
from ..models.user import User
from ..models.todo import Todo
from ..utils.errors import ValidationError, NotFoundError
from typing import Optional


class ConstraintValidator:
    """
    Class to handle database constraint validations.
    """
    
    @staticmethod
    def validate_user_exists(session: Session, user_id: int) -> bool:
        """
        Validate that a user exists before creating a related record.
        """
        user = session.get(User, user_id)
        return user is not None
    
    @staticmethod
    def validate_user_owns_todo(session: Session, user_id: int, todo_id: int) -> bool:
        """
        Validate that a user owns a specific todo.
        """
        todo = session.get(Todo, todo_id)
        if not todo:
            return False
        return todo.owner_id == user_id
    
    @staticmethod
    def validate_unique_email(session: Session, email: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Validate that an email is unique (excluding a specific user if provided).
        """
        query = select(User).where(User.email == email)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        
        result = session.exec(query)
        user = result.first()
        return user is None
    
    @staticmethod
    def validate_unique_username(session: Session, username: str, exclude_user_id: Optional[int] = None) -> bool:
        """
        Validate that a username is unique (excluding a specific user if provided).
        """
        query = select(User).where(User.username == username)
        if exclude_user_id:
            query = query.where(User.id != exclude_user_id)
        
        result = session.exec(query)
        user = result.first()
        return user is None
    
    @staticmethod
    def check_referential_integrity(session: Session, user_id: int) -> bool:
        """
        Check that referential integrity is maintained for a user.
        """
        # Check if user exists
        user = session.get(User, user_id)
        if not user:
            return False
        
        # All related todos should have valid references
        # This is enforced by the database foreign key constraints
        return True


def validate_user_ownership(session: Session, user_id: int, resource_id: int, resource_type: str) -> bool:
    """
    Generic function to validate user ownership of a resource.
    """
    if resource_type.lower() == "todo":
        return ConstraintValidator.validate_user_owns_todo(session, user_id, resource_id)
    else:
        raise ValueError(f"Unknown resource type: {resource_type}")


def validate_user_exists_or_raise(session: Session, user_id: int):
    """
    Validate that a user exists, raising an exception if not.
    """
    if not ConstraintValidator.validate_user_exists(session, user_id):
        raise NotFoundError("User", str(user_id))


def validate_unique_email_or_raise(session: Session, email: str, exclude_user_id: Optional[int] = None):
    """
    Validate that an email is unique, raising an exception if not.
    """
    if not ConstraintValidator.validate_unique_email(session, email, exclude_user_id):
        raise ValidationError(f"Email {email} already exists", "email")


def validate_unique_username_or_raise(session: Session, username: str, exclude_user_id: Optional[int] = None):
    """
    Validate that a username is unique, raising an exception if not.
    """
    if not ConstraintValidator.validate_unique_username(session, username, exclude_user_id):
        raise ValidationError(f"Username {username} already exists", "username")
