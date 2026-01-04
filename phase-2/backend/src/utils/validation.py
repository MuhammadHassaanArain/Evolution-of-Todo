"""
Validation utility functions for the validation hardening feature.

This module contains reusable validation functions for request payload validation,
including validation for unexpected fields, invalid data types, and payload size.
"""

import json
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, ValidationError
from fastapi import HTTPException
from ..models.validation import UNEXPECTED_FIELD_ERROR, VALIDATION_ERROR


def validate_request_payload(
    payload: Dict[str, Any],
    allowed_fields: List[str],
    max_payload_size: Optional[int] = None
) -> Dict[str, Any]:
    """
    Validate request payload for unexpected fields and size.

    Args:
        payload: The request payload to validate
        allowed_fields: List of field names that are allowed in the payload
        max_payload_size: Maximum size of the payload in bytes (optional)

    Returns:
        The validated payload

    Raises:
        HTTPException: If validation fails
    """
    if max_payload_size and len(json.dumps(payload)) > max_payload_size:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_003",
                    "message": "Request payload too large"
                }
            }
        )

    # Check for unexpected fields
    unexpected_fields = []
    for field in payload.keys():
        if field not in allowed_fields:
            unexpected_fields.append(field)

    if unexpected_fields:
        raise HTTPException(
            status_code=400,
            detail=UNEXPECTED_FIELD_ERROR
        )

    return payload


def validate_user_id_not_in_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that user_id is not present in the request payload.

    Args:
        payload: The request payload to validate

    Returns:
        The validated payload

    Raises:
        HTTPException: If user_id is found in the payload
    """
    if 'user_id' in payload:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_004",
                    "message": "user_id field not allowed in request payload"
                }
            }
        )

    return payload


def validate_data_types(payload: Dict[str, Any], expected_types: Dict[str, type]) -> Dict[str, Any]:
    """
    Validate that payload fields have the expected data types.

    Args:
        payload: The request payload to validate
        expected_types: Dictionary mapping field names to expected types

    Returns:
        The validated payload

    Raises:
        HTTPException: If data type validation fails
    """
    for field_name, expected_type in expected_types.items():
        if field_name in payload:
            actual_value = payload[field_name]
            if not isinstance(actual_value, expected_type):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": {
                            "code": "VALIDATION_005",
                            "message": f"Invalid data type for field '{field_name}'. Expected {expected_type.__name__}, got {type(actual_value).__name__}"
                        }
                    }
                )

    return payload


def validate_nested_payload_depth(payload: Any, max_depth: int = 10) -> None:
    """
    Validate that the payload doesn't have excessive nesting depth which could cause memory issues.

    Args:
        payload: The payload to validate (can be any JSON-serializable object)
        max_depth: Maximum allowed nesting depth

    Raises:
        HTTPException: If nesting depth exceeds the limit
    """
    def get_depth(obj, current_depth=0):
        if current_depth > max_depth:
            return current_depth

        if isinstance(obj, dict):
            if not obj:  # Empty dict has depth 1
                return current_depth + 1
            return max(get_depth(v, current_depth + 1) for v in obj.values())
        elif isinstance(obj, list):
            if not obj:  # Empty list has depth 1
                return current_depth + 1
            return max(get_depth(item, current_depth + 1) for item in obj)
        else:
            return current_depth

    depth = get_depth(payload)
    if depth > max_depth:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_006",
                    "message": f"Request payload nesting too deep. Maximum allowed depth is {max_depth}"
                }
            }
        )


def validate_payload_for_todos_update(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Specific validation function for todo update requests.
    Ensures no user_id is present and validates expected fields.

    Args:
        payload: The todo update request payload

    Returns:
        The validated payload
    """
    # Check that user_id is not in the payload
    validate_user_id_not_in_payload(payload)

    # Validate allowed fields for todo updates
    allowed_fields = ['title', 'description', 'completed']
    validate_request_payload(payload, allowed_fields)

    # Validate data types for specific fields
    expected_types = {
        'title': str,
        'description': str,
        'completed': bool
    }
    validate_data_types(payload, expected_types)

    # Validate payload depth
    validate_nested_payload_depth(payload)

    return payload


def validate_payload_for_todos_create(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Specific validation function for todo create requests.
    Ensures no user_id is present and validates expected fields.

    Args:
        payload: The todo create request payload

    Returns:
        The validated payload
    """
    # Check that user_id is not in the payload
    validate_user_id_not_in_payload(payload)

    # Validate allowed fields for todo creation
    allowed_fields = ['title', 'description']
    validate_request_payload(payload, allowed_fields)

    # Validate data types for specific fields
    expected_types = {
        'title': str,
        'description': str
    }
    validate_data_types(payload, expected_types)

    # Validate payload depth
    validate_nested_payload_depth(payload)

    # Title is required for creation
    if 'title' not in payload or not payload['title'] or not payload['title'].strip():
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_007",
                    "message": "title is required and cannot be empty"
                }
            }
        )

    # Validate title length (max 255 chars as per data model)
    if 'title' in payload and len(payload['title']) > 255:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_008",
                    "message": "title cannot exceed 255 characters"
                }
            }
        )

    # Validate description length (max 1000 chars as per data model)
    if 'description' in payload and len(payload['description']) > 1000:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_009",
                    "message": "description cannot exceed 1000 characters"
                }
            }
        )

    return payload


def validate_payload_size(payload: Dict[str, Any], max_size_bytes: int = 1024*1024) -> None:  # 1MB default
    """
    Validate the size of the payload to prevent oversized requests.

    Args:
        payload: The payload to validate
        max_size_bytes: Maximum allowed size in bytes (default 1MB)

    Raises:
        HTTPException: If payload size exceeds the limit
    """
    payload_str = json.dumps(payload)
    payload_size = len(payload_str.encode('utf-8'))

    if payload_size > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail={
                "error": {
                    "code": "VALIDATION_010",
                    "message": f"Request payload too large: {payload_size} bytes. Maximum allowed: {max_size_bytes} bytes"
                }
            }
        )