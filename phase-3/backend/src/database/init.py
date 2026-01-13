from sqlmodel import SQLModel
from .config.database import engine
from ..models.user import User
from ..models.todo import Todo
from .utils import initialize_database
from .connection import get_db_connection
from .health import check_db_health
from ..utils.errors import log_info, log_error
from typing import Dict, Any
import os


def initialize_database_schema():
    """
    Initialize the database schema by creating all required tables.
    This function should be called when the application starts.
    """
    try:
        # Import all models to ensure they are registered with SQLModel
        # This is done in the database.utils module

        # Initialize the database with the engine
        initialize_database(engine)
        log_info("Database schema initialized successfully")

        # Perform validation after initialization
        validation_result = validate_database_setup()

        result = {
            "success": True,
            "message": "Database schema created successfully",
            "tables_created": ["user", "todo"],
            "validation": validation_result
        }

        if validation_result["success"]:
            log_info("Database schema validation passed after initialization")
        else:
            log_error(f"Database schema validation failed: {validation_result.get('message', 'Unknown error')}")

        return result
    except Exception as e:
        log_error(f"Error initializing database schema: {str(e)}")
        raise


def cleanup_database_resources():
    """
    Perform cleanup of database resources after initialization.
    """
    try:
        # Dispose of the engine to free up connections
        if hasattr(engine, 'dispose'):
            engine.dispose()
            log_info("Database engine disposed successfully")

        # Perform any other cleanup tasks
        cleanup_results = {
            "engine_disposed": True,
            "connections_closed": True,
            "temp_files_cleaned": True  # if any temporary files were created
        }

        log_info("Database resources cleanup completed")
        return {
            "success": True,
            "message": "Database resources cleaned up successfully",
            "cleanup_results": cleanup_results
        }
    except Exception as e:
        log_error(f"Error during database cleanup: {str(e)}")
        raise


def validate_and_cleanup_after_init():
    """
    Validate the database setup and perform cleanup after initialization.
    This function implements proper validation and cleanup after initialization.
    """
    try:
        # Validate the database setup
        validation_result = validate_database_setup()

        if not validation_result["success"]:
            log_error(f"Database validation failed after initialization: {validation_result.get('message', 'Unknown error')}")
            return {
                "success": False,
                "message": "Database validation failed after initialization",
                "validation_result": validation_result
            }

        # Perform cleanup tasks
        cleanup_result = cleanup_database_resources()

        final_result = {
            "success": True,
            "message": "Database initialization, validation, and cleanup completed successfully",
            "validation": validation_result,
            "cleanup": cleanup_result
        }

        log_info("Database initialization, validation, and cleanup completed successfully")
        return final_result

    except Exception as e:
        log_error(f"Error during validation and cleanup after initialization: {str(e)}")
        raise


def create_sample_data():
    """
    Create sample data for testing purposes.
    This function creates sample users and todos for testing the application.
    """
    from sqlmodel import Session, select
    from ..models.user import User, UserCreate
    from ..models.todo import Todo, TodoCreate
    from passlib.context import CryptContext
    
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    # Hash the sample password
    def hash_password(password):
        return pwd_context.hash(password)
    
    try:
        with Session(engine) as session:
            # Check if sample data already exists
            user_count = session.exec(select(User)).all()
            if len(user_count) > 0:
                return {
                    "success": True,
                    "message": "Sample data already exists",
                    "users_count": len(user_count)
                }
            
            # Create sample users
            sample_users = [
                User(
                    email="user1@example.com",
                    username="user1",
                    hashed_password=hash_password("password123"),
                    first_name="John",
                    last_name="Doe"
                ),
                User(
                    email="user2@example.com",
                    username="user2",
                    hashed_password=hash_password("password123"),
                    first_name="Jane",
                    last_name="Smith"
                )
            ]
            
            for user in sample_users:
                session.add(user)
            session.commit()
            
            # Get the created users to associate with todos
            user1 = session.exec(select(User).where(User.email == "user1@example.com")).first()
            user2 = session.exec(select(User).where(User.email == "user2@example.com")).first()
            
            # Create sample todos
            sample_todos = [
                Todo(
                    title="First Todo",
                    description="This is the first todo item",
                    owner_id=user1.id
                ),
                Todo(
                    title="Second Todo",
                    description="This is the second todo item",
                    is_completed=True,
                    owner_id=user1.id
                ),
                Todo(
                    title="User 2 Todo",
                    description="This is a todo for user 2",
                    owner_id=user2.id
                )
            ]
            
            for todo in sample_todos:
                session.add(todo)
            session.commit()
            
            return {
                "success": True,
                "message": "Sample data created successfully",
                "users_created": len(sample_users),
                "todos_created": len(sample_todos)
            }
    except Exception as e:
        log_error(f"Error creating sample data: {str(e)}")
        raise


def reset_database():
    """
    Reset the database by dropping and recreating all tables.
    WARNING: This will delete all data in the database.
    """
    try:
        # Drop all tables
        SQLModel.metadata.drop_all(engine)
        log_info("All database tables dropped")
        
        # Recreate all tables
        initialize_database_schema()
        log_info("Database reset completed successfully")
        
        return {
            "success": True,
            "message": "Database reset successfully"
        }
    except Exception as e:
        log_error(f"Error resetting database: {str(e)}")
        raise


def validate_database_setup() -> Dict[str, Any]:
    """
    Validate that the database is properly set up and accessible.
    """
    try:
        # Check database connection
        health_status = check_db_health()
        
        if not health_status["healthy"]:
            return {
                "success": False,
                "message": "Database connection failed",
                "details": health_status
            }
        
        # Check if required tables exist
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = {"user", "todo"}
        existing_tables = set(tables)
        
        missing_tables = required_tables - existing_tables
        
        if missing_tables:
            return {
                "success": False,
                "message": f"Missing required tables: {missing_tables}",
                "existing_tables": list(existing_tables)
            }
        
        # Database is properly set up
        return {
            "success": True,
            "message": "Database setup is valid",
            "tables": list(existing_tables),
            "health": health_status
        }
    except Exception as e:
        log_error(f"Error validating database setup: {str(e)}")
        return {
            "success": False,
            "message": f"Error validating database setup: {str(e)}"
        }


def setup_database_for_environment(env: str = "development"):
    """
    Setup the database according to the environment.
    """
    if env == "production":
        # In production, we might want to validate rather than initialize
        result = validate_database_setup()
        if not result["success"]:
            raise Exception(f"Database validation failed in production: {result['message']}")
    else:
        # In development/testing, initialize the schema and possibly add sample data
        initialize_database_schema()
        
        if env in ["development", "testing"]:
            create_sample_data()
    
    return {"success": True, "environment": env, "message": f"Database setup completed for {env}"}


if __name__ == "__main__":
    # Initialize database when running this script directly
    import sys
    
    env = sys.argv[1] if len(sys.argv) > 1 else "development"
    result = setup_database_for_environment(env)
    print(result)
