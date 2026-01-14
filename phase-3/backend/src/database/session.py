from sqlmodel import Session, create_engine
from contextlib import contextmanager, AbstractContextManager
from typing import Generator, Optional
from ..config.settings import settings
from ..utils.errors import DatabaseError
import logging


class DatabaseSessionManager:
    """
    Manager for database sessions with ownership validation capabilities.
    """
    
    def __init__(self, database_url: Optional[str] = None):
        self.database_url = database_url or settings.database_url
        self.engine = create_engine(self.database_url)
        self.logger = logging.getLogger(__name__)
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """
        Get a database session with proper setup and cleanup.
        """
        session = Session(self.engine)
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            self.logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def get_session_context(self) -> AbstractContextManager[Session]:
        """
        Get a session context manager for use with 'with' statements.
        """
        return self.get_session()
    
    def validate_user_ownership(self, session: Session, user_id: int, resource_id: int, resource_type: str) -> bool:
        """
        Validate that a user owns a specific resource.
        This method checks ownership at the database level.
        """
        try:
            # Import models dynamically to avoid circular imports
            if resource_type.lower() == "todo":
                from ..models.todo import Todo
                resource = session.get(Todo, resource_id)
                if resource and resource.owner_id == user_id:
                    return True
            # Add more resource types as needed
            return False
        except Exception as e:
            self.logger.error(f"Ownership validation error: {e}")
            raise DatabaseError(f"Error validating ownership: {str(e)}")
    
    def execute_with_ownership_check(
        self, 
        user_id: int, 
        resource_id: int, 
        resource_type: str,
        operation: callable
    ) -> any:
        """
        Execute an operation with ownership validation.
        """
        with self.get_session() as session:
            # Validate ownership
            if not self.validate_user_ownership(session, user_id, resource_id, resource_type):
                raise PermissionError(f"User {user_id} does not own {resource_type} {resource_id}")
            
            # Execute the operation
            return operation(session)


# Global session manager instance
session_manager = DatabaseSessionManager()


def get_session() -> Generator[Session, None, None]:
    """
    Convenience function to get a database session.
    """
    with session_manager.get_session() as session:
        yield session


def validate_user_ownership(user_id: int, resource_id: int, resource_type: str) -> bool:
    """
    Convenience function to validate user ownership.
    """
    with session_manager.get_session() as session:
        return session_manager.validate_user_ownership(session, user_id, resource_id, resource_type)
