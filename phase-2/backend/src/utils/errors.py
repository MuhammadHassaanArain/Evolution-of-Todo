import logging
from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel
import traceback


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class APIError(BaseModel):
    """
    Standard API error response model.
    """
    detail: str
    error_code: Optional[str] = None
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR


class DatabaseError(Exception):
    """
    Custom exception for database-related errors.
    """
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(Exception):
    """
    Custom exception for validation errors.
    """
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class NotFoundError(Exception):
    """
    Custom exception for resource not found errors.
    """
    def __init__(self, resource_type: str, resource_id: str):
        self.message = f"{resource_type} with id {resource_id} not found"
        super().__init__(self.message)


def handle_database_error(error: Exception, context: str = "") -> DatabaseError:
    """
    Handle database errors and return a standardized error.
    """
    error_msg = f"Database error in {context}: {str(error)}"
    logger.error(error_msg)
    logger.error(traceback.format_exc())
    return DatabaseError(message=error_msg, error_code="DB_ERROR")


def handle_validation_error(error: Exception, context: str = "") -> ValidationError:
    """
    Handle validation errors and return a standardized error.
    """
    error_msg = f"Validation error in {context}: {str(error)}"
    logger.warning(error_msg)
    return ValidationError(message=error_msg)


def create_http_exception(
    status_code: int,
    detail: str,
    headers: Optional[dict] = None
) -> HTTPException:
    """
    Create an HTTP exception with the specified status code and detail.
    """
    logger.info(f"HTTP Exception: {status_code} - {detail}")
    return HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers
    )


def log_info(message: str):
    """
    Log an info message.
    """
    logger.info(message)


def log_warning(message: str):
    """
    Log a warning message.
    """
    logger.warning(message)


def log_error(message: str, exc_info: bool = True):
    """
    Log an error message.
    """
    logger.error(message, exc_info=exc_info)
