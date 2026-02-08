from sqlmodel import create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment, with a default for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/todo_app"
)

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False)

def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.
    """
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """
    Create database tables.
    This should be called when starting the application.
    """
    from models.user import User
    from models.todo import Todo
    from sqlmodel import SQLModel

    # Import all models here to ensure they're registered with SQLModel
    SQLModel.metadata.create_all(engine)