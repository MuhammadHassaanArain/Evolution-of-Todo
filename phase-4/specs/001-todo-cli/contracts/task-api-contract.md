# Task API Contract

## Overview
This document defines the contract for task operations in the Todo CLI application.

## Task Model
```python
class Task:
    id: int          # Unique identifier
    title: str       # Task title (required)
    description: str # Task description (optional)
    completed: bool  # Completion status (default: False)
```

## Service Functions

### add_task(title: str, description: str = "") -> dict
- **Purpose**: Add a new task to the in-memory list
- **Input**: title (required), description (optional)
- **Output**:
  ```python
  {
      "success": bool,
      "message": str,
      "task_id": int
  }
  ```
- **Errors**:
  - If title is empty: `{"success": False, "message": "Title is required"}`

### get_all_tasks() -> list[Task]
- **Purpose**: Retrieve all tasks from memory
- **Input**: None
- **Output**: List of Task objects

### get_task_by_id(task_id: int) -> Task | None
- **Purpose**: Retrieve a specific task by ID
- **Input**: task_id
- **Output**: Task object if found, None otherwise

### update_task(task_id: int, title: str = None, description: str = None) -> dict
- **Purpose**: Update task details
- **Input**: task_id (required), title (optional), description (optional)
- **Output**:
  ```python
  {
      "success": bool,
      "message": str
  }
  ```

### delete_task(task_id: int) -> dict
- **Purpose**: Delete a task by ID
- **Input**: task_id
- **Output**:
  ```python
  {
      "success": bool,
      "message": str
  }
  ```

### toggle_task_completion(task_id: int) -> dict
- **Purpose**: Toggle completion status of a task
- **Input**: task_id
- **Output**:
  ```python
  {
      "success": bool,
      "message": str,
      "completed": bool
  }
  ```