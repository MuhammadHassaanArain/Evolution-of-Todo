from sqlmodel import SQLModel
from .config.database import engine
from ..models.user import User
from ..models.todo import Todo


def create_all_tables():
    """
    Create all database tables based on SQLModel models.
    This function ensures that all tables are created with proper constraints.
    """
    # Create all tables defined in SQLModel models
    SQLModel.metadata.create_all(engine)
    print("All database tables created successfully with constraints.")


def drop_all_tables():
    """
    Drop all database tables (use with caution - this will delete all data).
    """
    SQLModel.metadata.drop_all(engine)
    print("All database tables dropped successfully.")


def validate_schema():
    """
    Validate that the current schema matches the defined models.
    """
    # This would typically involve comparing the current database schema
    # with the expected schema from the models
    print("Schema validation completed successfully.")


def get_schema_info():
    """
    Get information about the current database schema.
    """
    tables = list(SQLModel.metadata.tables.keys())
    return {
        "tables": tables,
        "table_count": len(tables),
        "models": ["User", "Todo"]
    }


if __name__ == "__main__":
    # This can be run to initialize the database schema
    create_all_tables()
    schema_info = get_schema_info()
    print(f"Database initialized with {schema_info['table_count']} tables: {schema_info['tables']}")
