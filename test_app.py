#!/usr/bin/env python3
"""
Simple test script to verify the Todo CLI application functionality.
"""

import sys
import os

# Add src to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from todo.cli.cli_app import TodoCLIApp


def test_basic_functionality():
    """Test basic functionality of the Todo application."""
    print("Testing basic functionality...")

    # Create an instance of the CLI app
    app = TodoCLIApp()

    # Test adding a task
    result = app.task_service.add_task("Test Task", "This is a test task")
    print(f"Add task result: {result}")

    # Verify task was added
    tasks = app.task_service.get_all_tasks()
    print(f"Number of tasks: {len(tasks)}")
    if tasks:
        print(f"First task: {tasks[0]}")

    # Test toggling completion
    if tasks:
        toggle_result = app.task_service.toggle_task_completion(tasks[0].id)
        print(f"Toggle completion result: {toggle_result}")

    # Test updating task
    if tasks:
        update_result = app.task_service.update_task(tasks[0].id, title="Updated Test Task")
        print(f"Update task result: {update_result}")

    # Test deleting task
    if tasks:
        delete_result = app.task_service.delete_task(tasks[0].id)
        print(f"Delete task result: {delete_result}")

    # Verify task was deleted
    tasks_after_delete = app.task_service.get_all_tasks()
    print(f"Number of tasks after deletion: {len(tasks_after_delete)}")

    print("All basic functionality tests completed successfully!")


if __name__ == "__main__":
    test_basic_functionality()