"""
Error response schemas for the validation hardening feature.

This module defines the standardized error response format used across all validation scenarios.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """
    Detailed error information structure.
    """
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """
    Standardized error response format.
    """
    error: ErrorDetail


class ValidationErrorResponse(BaseModel):
    """
    Response format specifically for validation errors.
    """
    error: ErrorDetail


# Predefined error responses for common scenarios

UNAUTHORIZED_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="AUTH_001",
        message="Invalid or expired token"
    )
)

MISSING_AUTH_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="AUTH_002",
        message="Missing authentication"
    )
)

VALIDATION_ERROR_RESPONSE = ValidationErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_001",
        message="Invalid request payload"
    )
)

UNEXPECTED_FIELD_RESPONSE = ValidationErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_002",
        message="Unexpected field in request"
    )
)

PERMISSION_DENIED_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="PERMISSION_001",
        message="Resource not found"
    )
)

RESOURCE_NOT_FOUND_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="RESOURCE_001",
        message="Resource not found"
    )
)

BAD_REQUEST_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_003",
        message="Bad request"
    )
)

PAYLOAD_TOO_LARGE_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_004",
        message="Request payload too large"
    )
)

INVALID_USER_ID_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_005",
        message="user_id field not allowed in request payload"
    )
)

INVALID_DATA_TYPE_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_006",
        message="Invalid data type in request"
    )
)

NESTED_TOO_DEEP_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_007",
        message="Request payload nesting too deep"
    )
)

TITLE_REQUIRED_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_008",
        message="title is required and cannot be empty"
    )
)

TITLE_TOO_LONG_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_009",
        message="title cannot exceed 255 characters"
    )
)

DESCRIPTION_TOO_LONG_RESPONSE = ErrorResponse(
    error=ErrorDetail(
        code="VALIDATION_010",
        message="description cannot exceed 1000 characters"
    )
)


def create_error_response(code: str, message: str, details: Optional[Dict[str, Any]] = None) -> ErrorResponse:
    """
    Helper function to create error responses dynamically.

    Args:
        code: Error code
        message: Error message
        details: Optional additional error details

    Returns:
        ErrorResponse instance
    """
    return ErrorResponse(
        error=ErrorDetail(
            code=code,
            message=message,
            details=details
        )
    )