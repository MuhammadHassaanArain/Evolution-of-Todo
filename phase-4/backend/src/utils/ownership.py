"""
Ownership validation utility functions for the validation hardening feature.

This module contains functions for validating that a user owns a specific resource,
enforcing ownership boundaries to prevent cross-user access.
"""

from sqlmodel import Session
from typing import Any, Optional
from fastapi import HTTPException
from ..models.validation import PERMISSION_DENIED_ERROR
from ..schemas.error import PERMISSION_DENIED_RESPONSE


def validate_user_ownership(
    session: Session,
    resource_id: str,
    user_id: str,
    resource_model_class: Any,
    user_id_field: str = "user_id"
) -> bool:
    """
    Validate that the given user owns the specified resource.

    Args:
        session: Database session
        resource_id: ID of the resource to check ownership for
        user_id: ID of the user claiming ownership
        resource_model_class: The SQLModel class of the resource
        user_id_field: Name of the field that stores the user ID (default: "user_id")

    Returns:
        True if the user owns the resource, raises HTTPException otherwise

    Raises:
        HTTPException: If the user does not own the resource
    """
    # Query the database to get the resource
    resource = session.get(resource_model_class, resource_id)

    if not resource:
        # Resource doesn't exist - return 404 (not found) to avoid information leakage
        raise HTTPException(
            status_code=404,
            detail=PERMISSION_DENIED_RESPONSE.dict()
        )

    # Get the owner's user_id from the resource
    resource_user_id = getattr(resource, user_id_field, None)

    if resource_user_id != user_id:
        # User doesn't own this resource - return 404 to avoid information leakage
        raise HTTPException(
            status_code=404,
            detail=PERMISSION_DENIED_RESPONSE.dict()
        )

    # User owns the resource
    return True


def check_user_owns_task(session: Session, task_id: str, user_id: str) -> bool:
    """
    Specific function to check if a user owns a specific task.

    Args:
        session: Database session
        task_id: ID of the task to check
        user_id: ID of the user to check ownership for

    Returns:
        True if the user owns the task, raises HTTPException otherwise
    """
    from ..models.task import Task

    return validate_user_ownership(
        session=session,
        resource_id=task_id,
        user_id=user_id,
        resource_model_class=Task,
        user_id_field="user_id"
    )


def check_user_owns_todo(session: Session, todo_id: str, user_id: str) -> bool:
    """
    Specific function to check if a user owns a specific todo.
    This is a placeholder that follows the same pattern as tasks.
    In a real implementation, this would work with a Todo model.

    Args:
        session: Database session
        todo_id: ID of the todo to check
        user_id: ID of the user to check ownership for

    Returns:
        True if the user owns the todo, raises HTTPException otherwise
    """
    from ..models.task import Task  # Using Task as Todo for this implementation

    return validate_user_ownership(
        session=session,
        resource_id=todo_id,
        user_id=user_id,
        resource_model_class=Task,  # Using Task model in this implementation
        user_id_field="user_id"
    )


def validate_ownership_before_operation(
    session: Session,
    resource_id: str,
    user_id: str,
    resource_model_class: Any,
    operation_name: str = "access",
    user_id_field: str = "user_id"
) -> None:
    """
    Validate ownership before performing an operation on a resource.
    This function combines ownership validation with logging.

    Args:
        session: Database session
        resource_id: ID of the resource to check
        user_id: ID of the user attempting the operation
        resource_model_class: The SQLModel class of the resource
        operation_name: Name of the operation being performed (for logging)
        user_id_field: Name of the field that stores the user ID

    Raises:
        HTTPException: If ownership validation fails
    """
    try:
        validate_user_ownership(
            session=session,
            resource_id=resource_id,
            user_id=user_id,
            resource_model_class=resource_model_class,
            user_id_field=user_id_field
        )
    except HTTPException:
        # Log the ownership validation failure
        from .logging import log_task_event
        log_task_event(
            f"ownership_validation_failed_{operation_name}",
            user_id=user_id,
            resource_id=resource_id,
            success=False,
            details={"operation": operation_name}
        )
        raise  # Re-raise the HTTPException


def validate_multiple_resources_ownership(
    session: Session,
    resource_ids: list,
    user_id: str,
    resource_model_class: Any,
    user_id_field: str = "user_id"
) -> list:
    """
    Validate that the user owns multiple resources.
    Returns the list of resource IDs that the user owns.

    Args:
        session: Database session
        resource_ids: List of resource IDs to check
        user_id: ID of the user to check ownership for
        resource_model_class: The SQLModel class of the resource
        user_id_field: Name of the field that stores the user ID

    Returns:
        List of resource IDs that the user owns

    Raises:
        HTTPException: If the user doesn't own any of the resources
    """
    valid_resource_ids = []

    for resource_id in resource_ids:
        try:
            validate_user_ownership(
                session=session,
                resource_id=resource_id,
                user_id=user_id,
                resource_model_class=resource_model_class,
                user_id_field=user_id_field
            )
            valid_resource_ids.append(resource_id)
        except HTTPException:
            # If any resource fails ownership validation, return 404 for all
            # This prevents information leakage about which specific resources exist
            raise HTTPException(
                status_code=404,
                detail=PERMISSION_DENIED_RESPONSE.dict()
            )

    return valid_resource_ids