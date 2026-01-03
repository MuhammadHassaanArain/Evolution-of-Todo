from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from contextlib import contextmanager
import logging
from ..config.settings import settings


def create_db_engine():
    """
    Create a database engine with the configured database URL.
    """
    return create_engine(settings.database_url)


def initialize_database(engine):
    """
    Initialize the database by creating all tables.
    """
    try:
        # Import models to register them with SQLModel before creating tables
        from ..models.user import User  # noqa: F401
        from ..models.todo import Todo  # noqa: F401
        
        SQLModel.metadata.create_all(engine)
        logging.info("Database tables created successfully")
    except Exception as e:
        logging.error(f"Error initializing database: {e}")
        raise


@contextmanager
def get_db_session(engine) -> Generator[Session, None, None]:
    """
    Context manager to get a database session.
    Ensures the session is properly closed after use.
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def test_connection(engine):
    """
    Test the database connection.
    """
    try:
        with engine.connect() as conn:
            # Test with a simple query
            result = conn.execute("SELECT 1")
            return result.fetchone()[0] == 1
    except Exception as e:
        logging.error(f"Database connection test failed: {e}")
        return False
