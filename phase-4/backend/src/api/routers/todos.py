from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from ...database.connection import get_session
from ...models.todo import Todo, TodoCreate
from ...schemas.todo import TodoCreate as TodoCreateSchema, TodoResponse, TodoUpdate
from ...services.todo_service import TodoService
from ...api.deps import get_current_user
from ...models.user import User
from ...utils.errors import handle_internal_error


# Create the router for todos endpoints
router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Todo not found"},
        422: {"description": "Validation error"}
    }
)


@router.post("/", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    todo_create: TodoCreateSchema
) -> TodoResponse:
    """
    Create a new todo for the authenticated user.
    The owner is derived from the JWT token, not the request body.
    """
    try:
        # Create the todo using the service
        db_todo = TodoService.create_todo(
            session=session,
            todo_create=TodoCreate(**todo_create.dict()),
            owner_id=current_user.id
        )
        
        # Convert to response schema
        return TodoResponse(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            is_completed=db_todo.is_completed,
            owner_id=db_todo.owner_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at
        )
    except Exception as e:
        return handle_internal_error(e, "creating todo")


@router.get("/", response_model=List[TodoResponse])
def read_todos(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[TodoResponse]:
    """
    Retrieve todos for the authenticated user.
    """
    try:
        # Get todos for the current user only
        todos = TodoService.get_todos_by_owner(
            session=session,
            owner_id=current_user.id,
            skip=skip,
            limit=limit
        )
        
        # Convert to response schema
        return [
            TodoResponse(
                id=todo.id,
                title=todo.title,
                description=todo.description,
                is_completed=todo.is_completed,
                owner_id=todo.owner_id,
                created_at=todo.created_at,
                updated_at=todo.updated_at
            )
            for todo in todos
        ]
    except Exception as e:
        return handle_internal_error(e, "reading todos")


@router.get("/{todo_id}", response_model=TodoResponse)
def read_todo(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    todo_id: int
) -> TodoResponse:
    """
    Get a specific todo by ID if it belongs to the authenticated user.
    """
    try:
        # Attempt to get the todo for the current user
        db_todo = TodoService.get_todo_by_id_for_user(
            session=session,
            todo_id=todo_id,
            user_id=current_user.id
        )
        
        if not db_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or not owned by user"
            )
        
        # Convert to response schema
        return TodoResponse(
            id=db_todo.id,
            title=db_todo.title,
            description=db_todo.description,
            is_completed=db_todo.is_completed,
            owner_id=db_todo.owner_id,
            created_at=db_todo.created_at,
            updated_at=db_todo.updated_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        return handle_internal_error(e, "reading specific todo")


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    todo_id: int,
    todo_update: TodoUpdate
) -> TodoResponse:
    """
    Update a specific todo if it belongs to the authenticated user.
    """
    try:
        # Get the todo for the current user
        db_todo = TodoService.get_todo_by_id_for_user(
            session=session,
            todo_id=todo_id,
            user_id=current_user.id
        )
        
        if not db_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or not owned by user"
            )
        
        # Update the todo
        updated_todo = TodoService.update_todo(
            session=session,
            todo=db_todo,
            todo_update=todo_update
        )
        
        # Convert to response schema
        return TodoResponse(
            id=updated_todo.id,
            title=updated_todo.title,
            description=updated_todo.description,
            is_completed=updated_todo.is_completed,
            owner_id=updated_todo.owner_id,
            created_at=updated_todo.created_at,
            updated_at=updated_todo.updated_at
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        return handle_internal_error(e, "updating todo")


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    *,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
    todo_id: int
) -> None:
    """
    Delete a specific todo if it belongs to the authenticated user.
    """
    try:
        # Get the todo for the current user
        db_todo = TodoService.get_todo_by_id_for_user(
            session=session,
            todo_id=todo_id,
            user_id=current_user.id
        )
        
        if not db_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or not owned by user"
            )
        
        # Delete the todo
        TodoService.delete_todo(session=session, todo=db_todo)
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        return handle_internal_error(e, "deleting todo")
