from sqlmodel import SQLModel
from typing import List, Optional
import logging
from pathlib import Path
from alembic.config import Config
from alembic.command import upgrade, revision, migrate
from alembic.script import ScriptDirectory
from alembic.runtime.environment import EnvironmentContext
import os


class DatabaseMigrationManager:
    """
    Manager for database migrations using Alembic.
    """
    
    def __init__(self, database_url: str, alembic_ini_path: Optional[str] = None):
        self.database_url = database_url
        self.alembic_ini_path = alembic_ini_path or self._create_alembic_config()
        self.logger = logging.getLogger(__name__)
        
    def _create_alembic_config(self) -> str:
        """
        Create a basic alembic configuration if one doesn't exist.
        """
        alembic_dir = Path("alembic")
        alembic_dir.mkdir(exist_ok=True)
        
        # Create alembic.ini file
        alembic_ini_content = f"""[alembic]
script_location = alembic
sqlalchemy.url = {self.database_url}

[post_write_hooks]
# Logging configuration
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %%(levelname)-5.5s [%%(name)s] %%(message)s
datefmt = %%H:%%M:%%S
"""
        
        alembic_ini_path = "alembic.ini"
        with open(alembic_ini_path, "w") as f:
            f.write(alembic_ini_content)
            
        # Create alembic directory structure
        versions_dir = alembic_dir / "versions"
        versions_dir.mkdir(exist_ok=True)
        
        # Create env.py
        env_py_content = f"""import asyncio
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from ...models.user import User
from ...models.todo import Todo

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here for 'autogenerate' support
target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={{"paramstyle": "named"}},
    )

    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
"""
        
        env_py_path = alembic_dir / "env.py"
        with open(env_py_path, "w") as f:
            f.write(env_py_content)
            
        # Create README for alembic
        readme_content = """# Alembic Migrations

This directory contains database migration scripts.

## Commands:
- `alembic revision --autogenerate -m "message"` - Create a new migration
- `alembic upgrade head` - Apply all migrations
- `alembic downgrade -1` - Rollback one migration
"""
        
        readme_path = alembic_dir / "README"
        with open(readme_path, "w") as f:
            f.write(readme_content)
        
        return alembic_ini_path
    
    def create_migration(self, message: str) -> str:
        """
        Create a new migration revision.
        """
        alembic_cfg = Config(self.alembic_ini_path)
        revision_kwargs = {
            "message": message,
            "autogenerate": True,
        }
        
        try:
            # This will create a new revision file
            revision(alembic_cfg, **revision_kwargs)
            self.logger.info(f"Created new migration: {message}")
            return "Migration created successfully"
        except Exception as e:
            self.logger.error(f"Error creating migration: {e}")
            raise
    
    def run_migrations(self, revision: str = "head"):
        """
        Run migrations to the specified revision (default: head/latest).
        """
        alembic_cfg = Config(self.alembic_ini_path)
        
        try:
            upgrade(alembic_cfg, revision)
            self.logger.info(f"Migrations applied up to revision: {revision}")
            return "Migrations applied successfully"
        except Exception as e:
            self.logger.error(f"Error running migrations: {e}")
            raise
    
    def get_current_revision(self) -> str:
        """
        Get the current database revision.
        """
        # This is a simplified implementation
        # In a real application, you'd query the alembic_version table
        return "current_revision"


# Convenience functions for common migration operations
def run_migrations_to_head(database_url: str):
    """
    Run all pending migrations to the head revision.
    """
    migration_manager = DatabaseMigrationManager(database_url)
    return migration_manager.run_migrations("head")


def create_initial_migration(database_url: str, message: str = "Initial migration"):
    """
    Create the initial migration based on current models.
    """
    migration_manager = DatabaseMigrationManager(database_url)
    return migration_manager.create_migration(message)
