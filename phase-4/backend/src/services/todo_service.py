from sqlmodel import Session, select
from typing import Optional, List
from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..utils.errors import handle_database_error, handle_not_found_error, handle_ownership_error
from ..models.user import User


class TodoService:
    """
    Service class for handling business logic related to Todo operations.
    """
    
    @staticmethod
    def create_todo(*, session: Session, todo_create: TodoCreate, owner_id: int) -> Todo:
        """
        Create a new todo for the specified owner.

        Args:
            session: Database session
            todo_create: Todo creation data
            owner_id: ID of the user who owns this todo

        Returns:
            Created Todo object
        """
        try:
            # Create the Todo object with the provided data and owner
            db_todo = Todo.from_orm(todo_create) if hasattr(todo_create, 'dict') else Todo(**todo_create.dict())
            db_todo.owner_id = owner_id
            
            # Add to session and commit
            session.add(db_todo)
            session.commit()
            session.refresh(db_todo)
            
            return db_todo
        except Exception as e:
            handle_database_error(e, "creating todo")
            raise
    
    @staticmethod
    def get_todo_by_id(*, session: Session, todo_id: int) -> Optional[Todo]:
        """
        Get a todo by its ID.

        Args:
            session: Database session
            todo_id: ID of the todo to retrieve

        Returns:
            Todo object if found, None otherwise
        """
        try:
            statement = select(Todo).where(Todo.id == todo_id)
            todo = session.exec(statement).first()
            return todo
        except Exception as e:
            handle_database_error(e, "getting todo by id")
            raise
    
    @staticmethod
    def get_todo_by_id_for_user(*, session: Session, todo_id: int, user_id: int) -> Optional[Todo]:
        """
        Get a todo by its ID for a specific user (ensuring ownership).

        Args:
            session: Database session
            todo_id: ID of the todo to retrieve
            user_id: ID of the requesting user

        Returns:
            Todo object if found and owned by user, None otherwise
        """
        try:
            statement = select(Todo).where(Todo.id == todo_id, Todo.owner_id == user_id)
            todo = session.exec(statement).first()
            return todo
        except Exception as e:
            handle_database_error(e, "getting todo by id for user")
            raise
    
    @staticmethod
    def get_todos_by_owner(*, session: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Get all todos for a specific owner.

        Args:
            session: Database session
            owner_id: ID of the owner whose todos to retrieve
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Todo objects belonging to the owner
        """
        try:
            statement = select(Todo).where(Todo.owner_id == owner_id).offset(skip).limit(limit)
            todos = session.exec(statement).all()
            return todos
        except Exception as e:
            handle_database_error(e, "getting todos by owner")
            raise
    
    @staticmethod
    def update_todo(*, session: Session, todo: Todo, todo_update: TodoUpdate) -> Todo:
        """
        Update a todo with new data.

        Args:
            session: Database session
            todo: Existing Todo object to update
            todo_update: New data for the todo

        Returns:
            Updated Todo object
        """
        try:
            # Get the update data as a dictionary
            update_data = todo_update.dict(exclude_unset=True)
            
            # Update the todo object with the new data
            for field, value in update_data.items():
                setattr(todo, field, value)
            
            # Update the updated_at timestamp
            from datetime import datetime
            todo.updated_at = datetime.utcnow()
            
            # Commit the changes
            session.add(todo)
            session.commit()
            session.refresh(todo)
            
            return todo
        except Exception as e:
            handle_database_error(e, "updating todo")
            raise
    
    @staticmethod
    def delete_todo(*, session: Session, todo: Todo) -> bool:
        """
        Delete a todo.

        Args:
            session: Database session
            todo: Todo object to delete

        Returns:
            True if deletion was successful
        """
        try:
            session.delete(todo)
            session.commit()
            return True
        except Exception as e:
            handle_database_error(e, "deleting todo")
            raise
    
    @staticmethod
    def check_ownership(*, session: Session, todo_id: int, user_id: int) -> bool:
        """
        Check if a user owns a specific todo.

        Args:
            session: Database session
            todo_id: ID of the todo to check
            user_id: ID of the user

        Returns:
            True if user owns the todo, False otherwise
        """
        try:
            todo = TodoService.get_todo_by_id_for_user(session=session, todo_id=todo_id, user_id=user_id)
            return todo is not None
        except Exception as e:
            handle_database_error(e, "checking ownership")
            raise


def create_todo_service(session: Session, todo_create: TodoCreate, owner_id: int) -> Todo:
    """
    Convenience function to create a todo using the service class.
    """
    return TodoService.create_todo(session=session, todo_create=todo_create, owner_id=owner_id)


def get_todo_by_id_service(session: Session, todo_id: int) -> Optional[Todo]:
    """
    Convenience function to get a todo by ID using the service class.
    """
    return TodoService.get_todo_by_id(session=session, todo_id=todo_id)


def get_todo_by_id_for_user_service(session: Session, todo_id: int, user_id: int) -> Optional[Todo]:
    """
    Convenience function to get a todo by ID for a specific user using the service class.
    """
    return TodoService.get_todo_by_id_for_user(session=session, todo_id=todo_id, user_id=user_id)


def get_todos_by_owner_service(session: Session, owner_id: int, skip: int = 0, limit: int = 100) -> List[Todo]:
    """
    Convenience function to get todos by owner using the service class.
    """
    return TodoService.get_todos_by_owner(session=session, owner_id=owner_id, skip=skip, limit=limit)


def update_todo_service(session: Session, todo: Todo, todo_update: TodoUpdate) -> Todo:
    """
    Convenience function to update a todo using the service class.
    """
    return TodoService.update_todo(session=session, todo=todo, todo_update=todo_update)


def delete_todo_service(session: Session, todo: Todo) -> bool:
    """
    Convenience function to delete a todo using the service class.
    """
    return TodoService.delete_todo(session=session, todo=todo)


def check_ownership_service(session: Session, todo_id: int, user_id: int) -> bool:
    """
    Convenience function to check ownership using the service class.
    """
    return TodoService.check_ownership(session=session, todo_id=todo_id, user_id=user_id)
