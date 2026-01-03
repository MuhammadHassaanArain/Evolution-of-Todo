from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import Optional
from ..models.user import User
from ..models.task import Task


class AuthorizationService:
    """
    Service to handle authorization checks and security validations
    """

    def check_user_owns_task(self, session: Session, user_id: str, task_id: str) -> bool:
        """
        Check if a user owns a specific task
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        return task is not None

    def enforce_user_owns_task(self, session: Session, user_id: str, task_id: str):
        """
        Enforce that a user owns a specific task, raising an exception if not
        """
        if not self.check_user_owns_task(session, user_id, task_id):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

    def check_user_active(self, session: Session, user_id: str) -> bool:
        """
        Check if a user is active
        """
        statement = select(User).where(User.id == user_id, User.is_active == True)
        user = session.exec(statement).first()
        return user is not None

    def enforce_user_active(self, session: Session, user_id: str):
        """
        Enforce that a user is active, raising an exception if not
        """
        if not self.check_user_active(session, user_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account is inactive"
            )

    def validate_token_scopes(self, token_scopes: list, required_scopes: list) -> bool:
        """
        Validate that the token has the required scopes
        """
        # For now, we'll implement a basic scope check
        # In a more complex system, this would check specific permissions
        if not required_scopes:
            return True  # No specific scopes required

        return all(scope in token_scopes for scope in required_scopes)


# Create a singleton instance of the AuthorizationService
authz_service = AuthorizationService()