"""
Database migration script for the Todo application
"""
from sqlmodel import SQLModel, create_engine
from src.config import settings
from src.models.user import User
from src.models.task import Task


def create_db_and_tables():
    """
    Create database tables based on SQLModel models
    """
    engine = create_engine(settings.database_url, echo=settings.db_echo)
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    create_db_and_tables()
    print("Database and tables created successfully!")