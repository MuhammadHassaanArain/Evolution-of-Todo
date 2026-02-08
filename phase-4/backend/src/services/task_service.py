from sqlmodel import Session, select
from typing import Optional, List
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
from ..utils.logging import log_task_event

class TaskService:
    def create_task(self, session: Session, task_create: TaskCreate, user_id: int) -> Task:
        """
        Create a new task for a user
        """
        db_task = Task(
            **task_create.model_dump(),
            user_id=user_id
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        log_task_event("task_created", user_id=user_id, task_id=str(db_task.id), success=True)
        return db_task

    def get_task_by_id(self, session: Session, task_id: str, user_id: int) -> Optional[Task]:
        """
        Get a task by ID for a specific user
        """
        from uuid import UUID
        try:
            uuid_task_id = UUID(task_id)
        except ValueError:
            # Invalid UUID format
            log_task_event("task_not_found", user_id=user_id, task_id=task_id, success=False, details={"reason": "invalid_uuid"})
            return None

        statement = select(Task).where(Task.id == uuid_task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if task:
            log_task_event("task_retrieved", user_id=user_id, task_id=task_id, success=True)
        else:
            log_task_event("task_not_found", user_id=user_id, task_id=task_id, success=False)
        return task

    def list_tasks(self, session: Session, user_id: int, offset: int = 0, limit: int = 100) -> List[Task]:
        """
        List tasks for a specific user with pagination
        """
        statement = select(Task).where(Task.user_id == user_id).offset(offset).limit(limit)
        tasks = session.exec(statement).all()
        log_task_event("tasks_listed", user_id=user_id, success=True, details={"count": len(tasks)})
        return tasks

    def update_task(self, session: Session, task_id: str, task_update: TaskUpdate, user_id: int) -> Optional[Task]:
        """
        Update a task for a specific user
        """
        from uuid import UUID
        try:
            uuid_task_id = UUID(task_id)
        except ValueError:
            # Invalid UUID format
            log_task_event("task_update_failed", user_id=user_id, task_id=task_id, success=False, details={"reason": "invalid_uuid"})
            return None

        statement = select(Task).where(Task.id == uuid_task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        if not db_task:
            log_task_event("task_update_failed", user_id=user_id, task_id=task_id, success=False, details={"reason": "task_not_found"})
            return None

        # Update the fields that were provided
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        log_task_event("task_updated", user_id=user_id, task_id=task_id, success=True)
        return db_task

    def delete_task(self, session: Session, task_id: str, user_id: int) -> bool:
        """
        Delete a task for a specific user
        """
        from uuid import UUID
        try:
            uuid_task_id = UUID(task_id)
        except ValueError:
            # Invalid UUID format
            log_task_event("task_delete_failed", user_id=user_id, task_id=task_id, success=False, details={"reason": "invalid_uuid"})
            return False

        statement = select(Task).where(Task.id == uuid_task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        if not db_task:
            log_task_event("task_delete_failed", user_id=user_id, task_id=task_id, success=False, details={"reason": "task_not_found"})
            return False

        session.delete(db_task)
        session.commit()
        log_task_event("task_deleted", user_id=user_id, task_id=task_id, success=True)
        return True

    def get_user_tasks_count(self, session: Session, user_id: int) -> int:
        """
        Get the count of tasks for a specific user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        log_task_event("tasks_count_retrieved", user_id=user_id, success=True, details={"count": len(tasks)})
        return len(tasks)


    def get_all_tasks(self, session: Session, offset: int = 0, limit: int = 100) -> List[Task]:
        """
        Get all tasks regardless of user (public access)
        """
        statement = select(Task).offset(offset).limit(limit)
        tasks = session.exec(statement).all()
        log_task_event("all_tasks_listed", user_id=None, success=True, details={"count": len(tasks)})
        return tasks

    def get_task_public(self, session: Session, task_id: str) -> Optional[Task]:
        """
        Get a task by ID without user restriction (public access)
        """
        from uuid import UUID
        try:
            uuid_task_id = UUID(task_id)
        except ValueError:
            # Invalid UUID format
            log_task_event("task_not_found", user_id=None, task_id=task_id, success=False, details={"reason": "invalid_uuid"})
            return None

        statement = select(Task).where(Task.id == uuid_task_id)
        task = session.exec(statement).first()
        if task:
            log_task_event("task_retrieved", user_id=None, task_id=task_id, success=True)
        else:
            log_task_event("task_not_found", user_id=None, task_id=task_id, success=False)
        return task

    def create_task_public(self, session: Session, task_create: TaskCreate) -> Task:
        """
        Create a task without user association (public access)
        Finds or creates a default system user for public tasks
        """
        from ..models.user import User

        # Try to get the first available user as the default for public tasks
        default_user = session.exec(select(User).limit(1)).first()
        if not default_user:
            # If no users exist, we'll use user_id 1 as default (assuming it exists)
            # This is a fallback - in a real system, you'd want to create a system user
            user_id = 1
        else:
            user_id = default_user.id

        db_task = Task(
            **task_create.model_dump(),
            user_id=user_id  # Use default user for public tasks
        )
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        log_task_event("public_task_created", user_id=None, task_id=str(db_task.id), success=True)
        return db_task

    def update_task_public(self, session: Session, task_id: str, task_update: TaskUpdate) -> Optional[Task]:
        """
        Update a task without user restriction (public access)
        """
        from uuid import UUID
        try:
            uuid_task_id = UUID(task_id)
        except ValueError:
            # Invalid UUID format
            log_task_event("task_update_failed", user_id=None, task_id=task_id, success=False, details={"reason": "invalid_uuid"})
            return None

        statement = select(Task).where(Task.id == uuid_task_id)
        db_task = session.exec(statement).first()
        if not db_task:
            log_task_event("task_update_failed", user_id=None, task_id=task_id, success=False, details={"reason": "task_not_found"})
            return None

        # Update the fields that were provided
        for field, value in task_update.model_dump(exclude_unset=True).items():
            setattr(db_task, field, value)

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        log_task_event("public_task_updated", user_id=None, task_id=task_id, success=True)
        return db_task

    def delete_task_public(self, session: Session, task_id: str) -> bool:
        """
        Delete a task without user restriction (public access)
        """
        from uuid import UUID
        try:
            uuid_task_id = UUID(task_id)
        except ValueError:
            # Invalid UUID format
            log_task_event("task_delete_failed", user_id=None, task_id=task_id, success=False, details={"reason": "invalid_uuid"})
            return False

        statement = select(Task).where(Task.id == uuid_task_id)
        db_task = session.exec(statement).first()
        if not db_task:
            log_task_event("task_delete_failed", user_id=None, task_id=task_id, success=False, details={"reason": "task_not_found"})
            return False

        session.delete(db_task)
        session.commit()
        log_task_event("public_task_deleted", user_id=None, task_id=task_id, success=True)
        return True


# Create a singleton instance of the TaskService
task_service = TaskService()