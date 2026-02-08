import os
import sys
from typing import Dict, Any
import argparse
from .init import initialize_database_schema, create_sample_data, reset_database, setup_database_for_environment
from .health import check_db_health
from .connection import test_db_connection
from ..utils.errors import log_info, log_error
from ..config.settings import settings


class DatabaseInitializationScript:
    """
    Class to handle database initialization scripts with environment support.
    """
    
    def __init__(self):
        self.supported_environments = ["development", "testing", "staging", "production"]
    
    def initialize_database(self, env: str = "development") -> Dict[str, Any]:
        """
        Initialize the database for a specific environment.
        """
        log_info(f"Initializing database for environment: {env}")
        
        try:
            if env not in self.supported_environments:
                raise ValueError(f"Unsupported environment: {env}. Supported: {self.supported_environments}")
            
            # Set environment-specific configurations
            os.environ["APP_ENV"] = env
            
            # Perform environment-specific setup
            result = setup_database_for_environment(env)
            
            log_info(f"Database initialization completed for environment: {env}")
            return result
            
        except Exception as e:
            log_error(f"Database initialization failed for environment {env}: {str(e)}")
            raise
    
    def validate_environment(self, env: str) -> bool:
        """
        Validate that the environment is supported.
        """
        return env in self.supported_environments
    
    def run_migrations(self) -> Dict[str, Any]:
        """
        Run database migrations.
        """
        log_info("Running database migrations...")
        
        try:
            # For now, we'll just initialize the schema
            # In a real application, this would run actual migrations
            result = initialize_database_schema()
            
            log_info("Database migrations completed successfully")
            return result
        except Exception as e:
            log_error(f"Database migrations failed: {str(e)}")
            raise
    
    def setup_for_environment(self, env: str) -> Dict[str, Any]:
        """
        Complete setup for a specific environment.
        """
        log_info(f"Setting up database for environment: {env}")
        
        try:
            # Validate environment
            if not self.validate_environment(env):
                raise ValueError(f"Invalid environment: {env}")
            
            # Run migrations
            migration_result = self.run_migrations()
            
            # Create sample data for non-production environments
            if env in ["development", "testing"]:
                sample_data_result = create_sample_data()
            else:
                sample_data_result = {"message": "Sample data creation skipped for production"}
            
            # Run health check
            health_result = check_db_health()
            
            result = {
                "environment": env,
                "migrations": migration_result,
                "sample_data": sample_data_result,
                "health_check": health_result,
                "setup_complete": True
            }
            
            log_info(f"Database setup completed for environment: {env}")
            return result
            
        except Exception as e:
            log_error(f"Database setup failed for environment {env}: {str(e)}")
            raise
    
    def reset_database(self) -> Dict[str, Any]:
        """
        Reset the database (for development/testing purposes).
        """
        log_info("Resetting database...")
        
        try:
            result = reset_database()
            log_info("Database reset completed")
            return result
        except Exception as e:
            log_error(f"Database reset failed: {str(e)}")
            raise
    
    def check_environment_readiness(self, env: str) -> Dict[str, Any]:
        """
        Check if the environment is ready for database operations.
        """
        try:
            # Check if database connection works
            connection_ok = test_db_connection()
            
            # Check health
            health_result = check_db_health()
            
            # Check if tables exist
            from .init import validate_database_setup
            setup_result = validate_database_setup()
            
            result = {
                "environment": env,
                "connection": connection_ok,
                "health": health_result,
                "setup_validated": setup_result,
                "ready": connection_ok and health_result["healthy"] and setup_result["success"]
            }
            
            return result
        except Exception as e:
            log_error(f"Environment readiness check failed: {str(e)}")
            raise


def main():
    """
    Main function to run the database initialization script.
    """
    parser = argparse.ArgumentParser(description="Database Initialization Script")
    parser.add_argument(
        "command",
        choices=["init", "migrate", "reset", "health", "ready", "setup"],
        help="Command to execute"
    )
    parser.add_argument(
        "--env",
        default="development",
        choices=["development", "testing", "staging", "production"],
        help="Environment to run in (default: development)"
    )
    
    args = parser.parse_args()
    
    script = DatabaseInitializationScript()
    
    try:
        if args.command == "init":
            result = script.initialize_database(args.env)
            print(f"Initialization completed: {result}")
        
        elif args.command == "migrate":
            result = script.run_migrations()
            print(f"Migrations completed: {result}")
        
        elif args.command == "reset":
            result = script.reset_database()
            print(f"Reset completed: {result}")
        
        elif args.command == "health":
            result = check_db_health()
            print(f"Health check: {result}")
        
        elif args.command == "ready":
            result = script.check_environment_readiness(args.env)
            print(f"Environment readiness: {result}")
        
        elif args.command == "setup":
            result = script.setup_for_environment(args.env)
            print(f"Setup completed: {result}")
        
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    
    except Exception as e:
        log_error(f"Script execution failed: {str(e)}")
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
