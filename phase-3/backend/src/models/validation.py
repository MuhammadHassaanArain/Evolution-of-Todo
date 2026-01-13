"""
Validation and error response models for the validation hardening feature.

This module defines the standardized error response format used across all validation scenarios.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel


class ValidationErrorResponse(BaseModel):
    """
    Standardized error response model for validation failures.
    """
    error: Dict[str, Any]

    class Config:
        # Allow extra fields for flexibility in error details
        extra = "allow"


class ErrorResponse(BaseModel):
    """
    Generic error response model with standardized structure.
    """
    error: Dict[str, Any]

    class Config:
        # Allow extra fields for flexibility in error details
        extra = "allow"


class ValidationErrorDetail(BaseModel):
    """
    Detailed validation error information.
    """
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ValidationErrorModel(BaseModel):
    """
    Model for validation errors with code, message and optional details.
    """
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


# Standard error response instances for common validation scenarios
UNAUTHORIZED_ERROR = {
    "error": {
        "code": "AUTH_001",
        "message": "Invalid or expired token"
    }
}

MISSING_AUTH_ERROR = {
    "error": {
        "code": "AUTH_002",
        "message": "Missing authentication"
    }
}

VALIDATION_ERROR = {
    "error": {
        "code": "VALIDATION_001",
        "message": "Invalid request payload"
    }
}

UNEXPECTED_FIELD_ERROR = {
    "error": {
        "code": "VALIDATION_002",
        "message": "Unexpected field in request"
    }
}

PERMISSION_DENIED_ERROR = {
    "error": {
        "code": "PERMISSION_001",
        "message": "Resource not found"
    }
}

RESOURCE_NOT_FOUND_ERROR = {
    "error": {
        "code": "RESOURCE_001",
        "message": "Resource not found"
    }
}