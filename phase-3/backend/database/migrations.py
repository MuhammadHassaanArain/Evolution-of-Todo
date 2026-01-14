"""
Database migration for Conversation and Message models
"""
from sqlmodel import SQLModel
from backend.database.conversation import Conversation
from backend.database.message import Message


def create_tables(engine):
    """
    Create all required tables for the chatbot functionality
    """
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")


def drop_tables(engine):
    """
    Drop all tables (use with caution!)
    """
    SQLModel.metadata.drop_all(engine)
    print("Tables dropped successfully!")


# Migration functions for alembic
def upgrade(engine):
    """
    Upgrade database to include Conversation and Message tables
    """
    create_tables(engine)


def downgrade(engine):
    """
    Downgrade database by removing Conversation and Message tables
    """
    drop_tables(engine)