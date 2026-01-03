from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import traceback
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIError(BaseModel):
    """
    Standard API error response model.
    """
    detail: str
    error_code: Optional[str] = None
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    timestamp: Optional[datetime] = None


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


class UnauthorizedError(Exception):
    """
    Custom exception for unauthorized access errors.
    """
    def __init__(self, message: str = "Unauthorized access"):
        self.message = message
        super().__init__(self.message)


class ForbiddenError(Exception):
    """
    Custom exception for forbidden access errors.
    """
    def __init__(self, message: str = "Forbidden access"):
        self.message = message
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
    headers: Optional[dict] = None,
    error_code: Optional[str] = None
) -> HTTPException:
    """
    Create an HTTP exception with the specified status code and detail.
    """
    logger.info(f"HTTP Exception: {status_code} - {detail}")
    if error_code:
        logger.info(f"Error code: {error_code}")
    return HTTPException(
        status_code=status_code,
        detail=detail,
        headers=headers
    )


def create_error_response(
    detail: str,
    error_code: Optional[str] = None,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
) -> Dict[str, Any]:
    """
    Create a standardized error response.
    """
    error_response = {
        "detail": detail,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if error_code:
        error_response["error_code"] = error_code
    
    return error_response


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


def handle_ownership_error(user_id: int, resource_owner_id: int, resource_type: str = "resource"):
    """
    Handle ownership validation errors.
    """
    error_detail = f"{resource_type} does not belong to user {user_id}"
    logger.warning(f"Ownership validation failed: user {user_id} tried to access {resource_type} owned by {resource_owner_id}")
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resource not found or not owned by user",
        error_code="OWNERSHIP_ERROR"
    )


def handle_not_found_error(resource_type: str, resource_id: str):
    """
    Handle resource not found errors.
    """
    error_detail = f"{resource_type} with id {resource_id} not found"
    logger.info(error_detail)
    return create_http_exception(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resource not found or not owned by user",
        error_code="NOT_FOUND"
    )


def handle_bad_request_error(detail: str):
    """
    Handle bad request errors.
    """
    logger.warning(f"Bad request: {detail}")
    return create_http_exception(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=detail,
        error_code="BAD_REQUEST"
    )


def handle_unauthorized_error(detail: str = "Not authenticated"):
    """
    Handle unauthorized access errors.
    """
    logger.warning(f"Unauthorized access: {detail}")
    return create_http_exception(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
        error_code="UNAUTHORIZED"
    )


def handle_forbidden_error(detail: str = "Access forbidden"):
    """
    Handle forbidden access errors.
    """
    logger.warning(f"Forbidden access: {detail}")
    return create_http_exception(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=detail,
        error_code="FORBIDDEN"
    )


def handle_internal_error(error: Exception, context: str = ""):
    """
    Handle internal server errors.
    """
    error_msg = f"Internal server error in {context}: {str(error)}"
    logger.error(error_msg)
    logger.error(traceback.format_exc())
    return create_http_exception(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error",
        error_code="INTERNAL_ERROR"
    )


# Common error responses
UNAUTHORIZED_RESPONSE = {
    "description": "Unauthorized",
    "content": {
        "application/json": {
            "example": {
                "detail": "Could not validate credentials",
                "error_code": "UNAUTHORIZED",
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }
    }
}

FORBIDDEN_RESPONSE = {
    "description": "Forbidden",
    "content": {
        "application/json": {
            "example": {
                "detail": "Access denied: Insufficient permissions",
                "error_code": "FORBIDDEN",
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }
    }
}

NOT_FOUND_RESPONSE = {
    "description": "Not Found",
    "content": {
        "application/json": {
            "example": {
                "detail": "Resource not found or not owned by user",
                "error_code": "NOT_FOUND",
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }
    }
}

BAD_REQUEST_RESPONSE = {
    "description": "Bad Request",
    "content": {
        "application/json": {
            "example": {
                "detail": "Invalid request body",
                "error_code": "BAD_REQUEST",
                "timestamp": "2023-01-01T12:00:00Z"
            }
        }
    }
}
