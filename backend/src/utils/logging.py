import logging
from datetime import datetime
from typing import Optional
from ..models.user import User


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with the specified name and level
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid adding multiple handlers if logger already exists
    if logger.handlers:
        return logger

    # Create console handler
    handler = logging.StreamHandler()
    handler.setLevel(level)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(handler)

    return logger


# Create loggers for different parts of the application
auth_logger = setup_logger("auth")
task_logger = setup_logger("task")
api_logger = setup_logger("api")


def log_auth_event(
    event_type: str,
    user: Optional[User] = None,
    ip_address: Optional[str] = None,
    success: bool = True,
    details: Optional[dict] = None
):
    """
    Log authentication events
    """
    user_id = user.id if user else "unknown"
    email = user.email if user else "unknown"

    log_data = {
        "event_type": event_type,
        "user_id": user_id,
        "email": email,
        "ip_address": ip_address,
        "success": success,
        "timestamp": datetime.utcnow().isoformat()
    }

    if details:
        log_data.update(details)

    message = f"AUTH_EVENT: {event_type} - User: {email} - Success: {success}"
    if not success:
        auth_logger.warning(f"{message} - Details: {log_data}")
    else:
        auth_logger.info(f"{message} - Details: {log_data}")


def log_task_event(
    event_type: str,
    user: Optional[User] = None,
    task_id: Optional[str] = None,
    success: bool = True,
    details: Optional[dict] = None
):
    """
    Log task-related events
    """
    user_id = user.id if user else "unknown"
    log_data = {
        "event_type": event_type,
        "user_id": user_id,
        "task_id": task_id,
        "success": success,
        "timestamp": datetime.utcnow().isoformat()
    }

    if details:
        log_data.update(details)

    message = f"TASK_EVENT: {event_type} - User: {user_id} - Task: {task_id} - Success: {success}"
    if not success:
        task_logger.warning(f"{message} - Details: {log_data}")
    else:
        task_logger.info(f"{message} - Details: {log_data}")