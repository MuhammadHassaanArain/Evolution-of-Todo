from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..database.session import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import UserRead
from ..services.task_service import task_service
from ..utils.logging import log_task_event
from ..utils.validation import validate_payload_for_todos_create, validate_payload_for_todos_update
from ..models.validation import PERMISSION_DENIED_ERROR, RESOURCE_NOT_FOUND_ERROR
from ..schemas.error import PERMISSION_DENIED_RESPONSE, RESOURCE_NOT_FOUND_RESPONSE

    
router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    offset: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """
    Get all public tasks
    """
    try:
        tasks = task_service.get_all_tasks(session, offset=offset, limit=limit)
        log_task_event("all_tasks_listed", user_id=None, success=True, details={"count": len(tasks)})
        return [TaskRead.from_orm(task) for task in tasks]
    except Exception as e:
        log_task_event("all_tasks_listed_failed", user_id=None, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new public task with validation hardening
    """
    try:
        # Convert the task to a dict for validation
        task_dict = task.dict()

        # Validate the payload for todo creation
        validate_payload_for_todos_create(task_dict)

        db_task = task_service.create_task_public(session, task)
        log_task_event("public_task_created", user_id=None, task_id=db_task.id, success=True)
        return TaskRead.from_orm(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("public_task_create_failed", user_id=None, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: str,
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID with validation hardening
    """
    try:
        db_task = task_service.get_task_public(session, task_id)
        if not db_task:
            log_task_event("task_not_found", user_id=None, task_id=task_id, success=False, details={"reason": "task_not_found"})
            # Return 404 for non-existent resources
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=RESOURCE_NOT_FOUND_RESPONSE.dict()
            )
        log_task_event("task_retrieved", user_id=None, task_id=task_id, success=True)
        return TaskRead.from_orm(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("task_retrieve_failed", user_id=None, task_id=task_id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    session: Session = Depends(get_session)
):
    """
    Update a specific task with validation hardening
    """
    try:
        # Convert the task_update to a dict for validation
        task_update_dict = task_update.dict(exclude_unset=True)

        # Validate the payload for todo updates
        validate_payload_for_todos_update(task_update_dict)

        db_task = task_service.update_task_public(session, task_id, task_update)
        if not db_task:
            log_task_event("task_update_failed", user_id=None, task_id=task_id, success=False, details={"reason": "task_not_found"})
            # Return 404 for non-existent resources
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=RESOURCE_NOT_FOUND_RESPONSE.dict()
            )
        log_task_event("public_task_updated", user_id=None, task_id=task_id, success=True)
        return TaskRead.from_orm(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("public_task_update_failed", user_id=None, task_id=task_id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )


@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
def complete_task(
    task_id: str,
    session: Session = Depends(get_session)
):
    """
    Mark a specific task as completed
    """
    try:
        # Check if the task exists
        db_task = task_service.get_task_public(session, task_id)
        if not db_task:
            log_task_event("task_complete_failed", user_id=None, task_id=task_id, success=False, details={"reason": "task_not_found"})
            # Return 404 for non-existent resources
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=RESOURCE_NOT_FOUND_RESPONSE.dict()
            )

        # If already completed, return success (idempotent behavior)
        if db_task.is_completed:
            log_task_event("task_already_completed", user_id=None, task_id=task_id, success=True)
            return TaskRead.from_orm(db_task)

        # Update the task to mark as completed
        task_update = TaskUpdate(is_completed=True)
        updated_db_task = task_service.update_task_public(session, task_id, task_update)
        if not updated_db_task:
            log_task_event("task_complete_failed", user_id=None, task_id=task_id, success=False, details={"reason": "task_not_found_after_validation"})
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=RESOURCE_NOT_FOUND_RESPONSE.dict()
            )

        log_task_event("public_task_completed", user_id=None, task_id=task_id, success=True)
        return TaskRead.from_orm(updated_db_task)
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("public_task_complete_failed", user_id=None, task_id=task_id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to complete task"
        )


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: str,
    session: Session = Depends(get_session)
):
    """
    Delete a specific task with validation hardening
    """
    try:
        success = task_service.delete_task_public(session, task_id)
        if not success:
            log_task_event("task_delete_failed", user_id=None, task_id=task_id, success=False, details={"reason": "task_not_found"})
            # Return 404 for non-existent resources
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=RESOURCE_NOT_FOUND_RESPONSE.dict()
            )
        log_task_event("public_task_deleted", user_id=None, task_id=task_id, success=True)
        return {"message": "Task deleted successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("public_task_delete_failed", user_id=None, task_id=task_id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )