from sqlmodel import create_engine
from sqlalchemy import event
from sqlalchemy.pool import Pool
from typing import Optional
import time
import logging
from ..config.settings import settings


class DatabaseConnectionManager:
    """
    Manager for database connections with proper handling and optimization.
    """
    
    def __init__(self, database_url: Optional[str] = None, pool_size: int = 5, max_overflow: int = 10):
        self.database_url = database_url or settings.database_url
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.engine = None
        self.logger = logging.getLogger(__name__)
        self._create_engine()
    
    def _create_engine(self):
        """
        Create the database engine with proper configuration.
        """
        try:
            # Create engine with connection pooling and other optimizations
            self.engine = create_engine(
                self.database_url,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                pool_pre_ping=True,  # Verify connections before use
                pool_recycle=300,    # Recycle connections every 5 minutes
                echo=False           # Set to True for SQL debugging
            )
            
            # Add connection events for monitoring
            @event.listens_for(self.engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                """
                Set SQLite pragmas if using SQLite (for compatibility).
                """
                if "sqlite" in self.database_url:
                    cursor = dbapi_connection.cursor()
                    cursor.execute("PRAGMA foreign_keys=ON")
                    cursor.close()
            
            self.logger.info(f"Database engine created successfully for URL: {self.database_url.replace('@', '[@]').replace(':', '[:]').split('@')[-1] if '@' in self.database_url else self.database_url}")
            
        except Exception as e:
            self.logger.error(f"Error creating database engine: {e}")
            raise
    
    def get_engine(self):
        """
        Get the database engine instance.
        """
        if not self.engine:
            self._create_engine()
        return self.engine
    
    def test_connection(self) -> bool:
        """
        Test the database connection.
        """
        try:
            with self.engine.connect() as connection:
                # Execute a simple query to test the connection
                result = connection.execute("SELECT 1")
                return result.fetchone()[0] == 1
        except Exception as e:
            self.logger.error(f"Database connection test failed: {e}")
            return False
    
    def get_connection_stats(self) -> dict:
        """
        Get connection pool statistics.
        """
        if not self.engine:
            return {"error": "Engine not initialized"}
        
        pool = self.engine.pool
        return {
            "pool_size": pool.size(),
            "checked_out": pool.checkedout(),
            "overflow": pool.overflow(),
            "pool_timeout": pool.timeout
        }
    
    def dispose_engine(self):
        """
        Dispose of the database engine.
        """
        if self.engine:
            self.engine.dispose()
            self.logger.info("Database engine disposed")


def get_db_connection():
    """
    Get a database connection using the connection manager.
    """
    manager = DatabaseConnectionManager()
    return manager.get_engine()


def test_db_connection() -> bool:
    """
    Test the database connection.
    """
    manager = DatabaseConnectionManager()
    return manager.test_connection()


# Global connection manager instance
connection_manager = DatabaseConnectionManager(
    database_url=settings.database_url,
    pool_size=5,
    max_overflow=10
)


def get_engine():
    """
    Get the global database engine instance.
    """
    return connection_manager.get_engine()


def get_connection_stats():
    """
    Get global connection statistics.
    """
    return connection_manager.get_connection_stats()


if __name__ == "__main__":
    # Test the connection when running this script directly
    print("Testing database connection...")
    success = test_db_connection()
    print(f"Connection test: {'PASSED' if success else 'FAILED'}")
    
    stats = get_connection_stats()
    print(f"Connection stats: {stats}")
