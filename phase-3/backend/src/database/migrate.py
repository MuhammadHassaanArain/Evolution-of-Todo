"""
Database migration script for the Todo application
"""
from sqlmodel import SQLModel, create_engine
from .config import settings
from ..models.user import User
from ..models.task import Task


def create_db_and_tables():
    """
    Create database tables based on SQLModel models
    """
    engine = create_engine(settings.database_url, echo=settings.db_echo)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully!")