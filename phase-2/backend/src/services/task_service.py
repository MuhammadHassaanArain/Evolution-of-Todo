from sqlmodel import Session, select
from typing import Optional, List
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
from ..utils.logging import log_task_event


class TaskService:
    def create_task(self, session: Session, task_create: TaskCreate, user_id: str) -> Task:
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
        log_task_event("task_created", user_id=user_id, task_id=db_task.id, success=True)
        return db_task

    def get_task_by_id(self, session: Session, task_id: str, user_id: str) -> Optional[Task]:
        """
        Get a task by ID for a specific user
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if task:
            log_task_event("task_retrieved", user_id=user_id, task_id=task_id, success=True)
        else:
            log_task_event("task_not_found", user_id=user_id, task_id=task_id, success=False)
        return task

    def list_tasks(self, session: Session, user_id: str, offset: int = 0, limit: int = 100) -> List[Task]:
        """
        List tasks for a specific user with pagination
        """
        statement = select(Task).where(Task.user_id == user_id).offset(offset).limit(limit)
        tasks = session.exec(statement).all()
        log_task_event("tasks_listed", user_id=user_id, success=True, details={"count": len(tasks)})
        return tasks

    def update_task(self, session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> Optional[Task]:
        """
        Update a task for a specific user
        """
        db_task = self.get_task_by_id(session, task_id, user_id)
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

    def delete_task(self, session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a task for a specific user
        """
        db_task = self.get_task_by_id(session, task_id, user_id)
        if not db_task:
            log_task_event("task_delete_failed", user_id=user_id, task_id=task_id, success=False, details={"reason": "task_not_found"})
            return False

        session.delete(db_task)
        session.commit()
        log_task_event("task_deleted", user_id=user_id, task_id=task_id, success=True)
        return True

    def get_user_tasks_count(self, session: Session, user_id: str) -> int:
        """
        Get the count of tasks for a specific user
        """
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        log_task_event("tasks_count_retrieved", user_id=user_id, success=True, details={"count": len(tasks)})
        return len(tasks)


# Create a singleton instance of the TaskService
task_service = TaskService()