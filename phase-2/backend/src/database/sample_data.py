from sqlmodel import Session, select
from typing import Dict, Any, List
from .connection import get_engine
from ..models.user import User, UserCreate
from ..models.todo import Todo, TodoCreate
from ..utils.errors import log_info, log_error
from passlib.context import CryptContext


class SampleDataCreator:
    """
    Class to create sample data for testing and development purposes.
    """
    
    def __init__(self):
        self.engine = get_engine()
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.created_users = []
        self.created_todos = []
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using the configured password context.
        """
        return self.pwd_context.hash(password)
    
    def create_sample_users(self, count: int = 2) -> List[User]:
        """
        Create sample users for testing.
        """
        users_data = [
            {
                "email": f"user{i}@example.com",
                "username": f"user{i}",
                "first_name": f"First{i}",
                "last_name": f"Last{i}",
                "hashed_password": self.hash_password("password123")
            }
            for i in range(1, count + 1)
        ]
        
        sample_users = []
        
        with Session(self.engine) as session:
            # Check if sample users already exist
            existing_users = session.exec(select(User)).all()
            if existing_users:
                log_info(f"Found {len(existing_users)} existing users, skipping sample user creation")
                return existing_users
            
            # Create new users
            for user_data in users_data:
                user = User(**user_data)
                session.add(user)
                sample_users.append(user)
            
            session.commit()
            
            # Refresh to get IDs
            for user in sample_users:
                session.refresh(user)
        
        self.created_users = sample_users
        log_info(f"Created {len(sample_users)} sample users")
        return sample_users
    
    def create_sample_todos(self, count: int = 3) -> List[Todo]:
        """
        Create sample todos for testing.
        """
        with Session(self.engine) as session:
            # Get all users (or create sample users if none exist)
            users = session.exec(select(User)).all()
            if not users:
                users = self.create_sample_users()
            
            # Check if sample todos already exist
            existing_todos = session.exec(select(Todo)).all()
            if existing_todos:
                log_info(f"Found {len(existing_todos)} existing todos, skipping sample todo creation")
                return existing_todos
            
            # Create sample todos
            sample_todos = []
            todo_descriptions = [
                "Complete the project documentation",
                "Review code with team",
                "Prepare for demo",
                "Update dependencies",
                "Fix reported bugs",
                "Write unit tests"
            ]
            
            for i in range(count):
                user = users[i % len(users)]  # Distribute todos among users
                todo = Todo(
                    title=f"Sample Todo {i+1}",
                    description=todo_descriptions[i % len(todo_descriptions)],
                    is_completed=(i % 3 == 0),  # Every third todo is completed
                    owner_id=user.id
                )
                session.add(todo)
                sample_todos.append(todo)
            
            session.commit()
            
            # Refresh to get IDs
            for todo in sample_todos:
                session.refresh(todo)
        
        self.created_todos = sample_todos
        log_info(f"Created {len(sample_todos)} sample todos")
        return sample_todos
    
    def create_complete_sample_data(self) -> Dict[str, Any]:
        """
        Create complete sample data including users and todos.
        """
        try:
            users = self.create_sample_users()
            todos = self.create_sample_todos()
            
            result = {
                "success": True,
                "users_created": len(users),
                "todos_created": len(todos),
                "total_resources": len(users) + len(todos),
                "sample_data": {
                    "users": [user.username for user in users],
                    "todos": [todo.title for todo in todos]
                }
            }
            
            log_info(f"Complete sample data created: {len(users)} users, {len(todos)} todos")
            return result
            
        except Exception as e:
            log_error(f"Error creating sample data: {str(e)}")
            raise
    
    def clear_sample_data(self) -> Dict[str, Any]:
        """
        Clear all sample data (for testing purposes).
        """
        with Session(self.engine) as session:
            # Delete all todos first (due to foreign key constraints)
            session.exec(select(Todo).where(Todo.id.in_([todo.id for todo in self.created_todos])))
            
            # Delete all users
            session.exec(select(User).where(User.id.in_([user.id for user in self.created_users])))
            
            session.commit()
        
        log_info(f"Sample data cleared: {len(self.created_todos)} todos, {len(self.created_users)} users")
        return {
            "success": True,
            "users_deleted": len(self.created_users),
            "todos_deleted": len(self.created_todos)
        }
    
    def validate_sample_data(self) -> Dict[str, Any]:
        """
        Validate that sample data exists and is consistent.
        """
        with Session(self.engine) as session:
            users = session.exec(select(User)).all()
            todos = session.exec(select(Todo)).all()
            
            # Check that all todos have valid owners
            valid_todos = 0
            for todo in todos:
                user_exists = session.get(User, todo.owner_id) is not None
                if user_exists:
                    valid_todos += 1
            
            result = {
                "users_count": len(users),
                "todos_count": len(todos),
                "valid_todos": valid_todos,
                "orphaned_todos": len(todos) - valid_todos,
                "validation_passed": len(todos) == valid_todos
            }
            
            return result


def create_sample_data() -> Dict[str, Any]:
    """
    Convenience function to create sample data.
    """
    creator = SampleDataCreator()
    return creator.create_complete_sample_data()


def validate_sample_data() -> Dict[str, Any]:
    """
    Convenience function to validate sample data.
    """
    creator = SampleDataCreator()
    return creator.validate_sample_data()


def clear_sample_data() -> Dict[str, Any]:
    """
    Convenience function to clear sample data.
    """
    creator = SampleDataCreator()
    return creator.clear_sample_data()


# Global sample data creator instance
sample_data_creator = SampleDataCreator()


if __name__ == "__main__":
    print("Creating sample data...")
    result = create_sample_data()
    print(f"Sample data creation result: {result}")
    
    print("\nValidating sample data...")
    validation_result = validate_sample_data()
    print(f"Validation result: {validation_result}")
    
    print("\nSample data created successfully!")
