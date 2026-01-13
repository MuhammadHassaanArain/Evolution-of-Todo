from typing import Dict, Any
from ..config.settings import settings
from .connection import get_engine, test_db_connection
from ..utils.errors import log_info, log_error
import time
from datetime import datetime


class DatabaseHealthChecker:
    """
    Class to check the health of the database connection and performance.
    """
    
    def __init__(self):
        self.engine = get_engine()
        self.last_check_time = None
        self.last_check_result = None
    
    def check_health(self) -> Dict[str, Any]:
        """
        Perform a comprehensive health check on the database.
        """
        start_time = time.time()
        
        try:
            # Test basic connectivity
            connectivity_ok = test_db_connection()
            
            # Measure response time
            response_time = time.time() - start_time
            
            # Get additional metrics
            metrics = self._get_db_metrics()
            
            # Overall health status
            healthy = connectivity_ok and response_time < 1.0  # Less than 1 second
            
            result = {
                "healthy": healthy,
                "timestamp": datetime.utcnow().isoformat(),
                "connectivity": {
                    "status": "OK" if connectivity_ok else "FAILED",
                    "response_time_seconds": response_time
                },
                "metrics": metrics,
                "performance": {
                    "response_time_threshold_ok": response_time < 1.0,
                    "response_time_seconds": response_time
                }
            }
            
            self.last_check_time = datetime.utcnow()
            self.last_check_result = result
            
            log_info(f"Database health check completed. Healthy: {healthy}, Response time: {response_time:.3f}s")
            return result
            
        except Exception as e:
            log_error(f"Database health check failed: {str(e)}")
            result = {
                "healthy": False,
                "timestamp": datetime.utcnow().isoformat(),
                "error": str(e),
                "connectivity": {
                    "status": "ERROR",
                    "response_time_seconds": time.time() - start_time
                }
            }
            return result
    
    def _get_db_metrics(self) -> Dict[str, Any]:
        """
        Get additional database metrics.
        """
        try:
            from sqlmodel import text
            with self.engine.connect() as conn:
                # Get basic database info
                db_info = {}
                
                # For PostgreSQL
                if "postgresql" in settings.database_url.lower():
                    result = conn.execute(text("SELECT version();"))
                    version = result.fetchone()
                    if version:
                        db_info["version"] = version[0]
                    
                    # Check active connections
                    result = conn.execute(text("SELECT count(*) FROM pg_stat_activity;"))
                    connections = result.fetchone()
                    if connections:
                        db_info["active_connections"] = connections[0]
                
                # For SQLite (for testing)
                elif "sqlite" in settings.database_url.lower():
                    result = conn.execute(text("SELECT sqlite_version();"))
                    version = result.fetchone()
                    if version:
                        db_info["version"] = version[0]
                
                return db_info
        except Exception as e:
            log_error(f"Error getting database metrics: {str(e)}")
            return {"error": str(e)}
    
    def get_health_status(self) -> Dict[str, Any]:
        """
        Get the last health check result or perform a new check if none exists.
        """
        if self.last_check_result is None:
            return self.check_health()
        return self.last_check_result
    
    def is_healthy(self) -> bool:
        """
        Check if the database is healthy.
        """
        result = self.get_health_status()
        return result.get("healthy", False)


def check_db_health() -> Dict[str, Any]:
    """
    Convenience function to check database health.
    """
    checker = DatabaseHealthChecker()
    return checker.check_health()


def is_db_healthy() -> bool:
    """
    Convenience function to check if database is healthy.
    """
    checker = DatabaseHealthChecker()
    return checker.is_healthy()


def get_db_metrics() -> Dict[str, Any]:
    """
    Convenience function to get database metrics.
    """
    checker = DatabaseHealthChecker()
    return checker._get_db_metrics()


# Global health checker instance
health_checker = DatabaseHealthChecker()


def get_health_status() -> Dict[str, Any]:
    """
    Get health status from the global instance.
    """
    return health_checker.get_health_status()


def ping_db() -> Dict[str, Any]:
    """
    Simple ping to check if the database is responding.
    """
    result = check_db_health()
    return {
        "status": "healthy" if result["healthy"] else "unhealthy",
        "timestamp": result["timestamp"],
        "response_time": result["connectivity"]["response_time_seconds"]
    }


if __name__ == "__main__":
    # Run health check when executing this script directly
    print("Performing database health check...")
    health_result = check_db_health()
    
    print(f"Healthy: {health_result['healthy']}")
    print(f"Timestamp: {health_result['timestamp']}")
    print(f"Response time: {health_result['connectivity']['response_time_seconds']:.3f}s")
    
    if "error" in health_result:
        print(f"Error: {health_result['error']}")
    
    print(f"Metrics: {health_result.get('metrics', {})}")
