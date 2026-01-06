from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ..database.session import get_session
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import UserRead
from ..services.task_service import task_service
from .auth_dependency import get_current_user
from ..utils.logging import log_task_event
from ..utils.validation import validate_payload_for_todos_create, validate_payload_for_todos_update
from ..models.validation import PERMISSION_DENIED_ERROR, RESOURCE_NOT_FOUND_ERROR
from ..schemas.error import PERMISSION_DENIED_RESPONSE, RESOURCE_NOT_FOUND_RESPONSE


router = APIRouter()


@router.get("/tasks", response_model=List[TaskRead])
def get_tasks(
    offset: int = 0,
    limit: int = 100,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the current user
    """
    try:
        tasks = task_service.list_tasks(session, current_user.id, offset=offset, limit=limit)
        log_task_event("tasks_listed", user_id=current_user.id, success=True, details={"count": len(tasks)})
        return [TaskRead.from_orm(task) for task in tasks]
    except Exception as e:
        log_task_event("tasks_list_failed", user_id=current_user.id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks"
        )


@router.post("/tasks", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current user with validation hardening
    """
    try:
        # Convert the task to a dict for validation
        task_dict = task.dict()

        # Validate the payload for todo creation
        validate_payload_for_todos_create(task_dict)

        db_task = task_service.create_task(session, task, current_user.id)
        log_task_event("task_created", user_id=current_user.id, task_id=db_task.id, success=True)
        return TaskRead.from_orm(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("task_create_failed", user_id=current_user.id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task"
        )


@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(
    task_id: str,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID for the current user with validation hardening
    """
    try:
        db_task = task_service.get_task_by_id(session, task_id, current_user.id)
        if not db_task:
            log_task_event("task_access_denied", user_id=current_user.id, task_id=task_id, success=False, details={"reason": "task_not_found_or_not_owned"})
            # Return 404 for non-owned resources (ownership enforcement)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=RESOURCE_NOT_FOUND_RESPONSE.dict()
            )
        log_task_event("task_retrieved", user_id=current_user.id, task_id=task_id, success=True)
        return TaskRead.from_orm(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("task_retrieve_failed", user_id=current_user.id, task_id=task_id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task"
        )


@router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task for the current user with validation hardening
    """
    try:
        # Convert the task_update to a dict for validation
        task_update_dict = task_update.dict(exclude_unset=True)

        # Validate the payload for todo updates
        validate_payload_for_todos_update(task_update_dict)

        db_task = task_service.update_task(session, task_id, task_update, current_user.id)
        if not db_task:
            log_task_event("task_update_failed", user_id=current_user.id, task_id=task_id, success=False, details={"reason": "task_not_found"})
            # Return 404 for non-owned resources (ownership enforcement)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=RESOURCE_NOT_FOUND_RESPONSE.dict()
            )
        log_task_event("task_updated", user_id=current_user.id, task_id=task_id, success=True)
        return TaskRead.from_orm(db_task)
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("task_update_failed", user_id=current_user.id, task_id=task_id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task"
        )


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: str,
    current_user: UserRead = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task for the current user with validation hardening
    """
    try:
        success = task_service.delete_task(session, task_id, current_user.id)
        if not success:
            log_task_event("task_delete_failed", user_id=current_user.id, task_id=task_id, success=False, details={"reason": "task_not_found_or_not_owned"})
            # Return 404 for non-owned resources (ownership enforcement)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=RESOURCE_NOT_FOUND_RESPONSE.dict()
            )
        log_task_event("task_deleted", user_id=current_user.id, task_id=task_id, success=True)
        return {"message": "Task deleted successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions (like validation errors)
        raise
    except Exception as e:
        log_task_event("task_delete_failed", user_id=current_user.id, task_id=task_id, success=False, details={"error": str(e)})
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task"
        )