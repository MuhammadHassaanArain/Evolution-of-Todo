"""
CLI Application

This module implements the command-line interface for the Todo application.
It provides a menu-driven interface for users to interact with their tasks.
"""

from typing import Optional
from todo.services.task_service import TaskService


class TodoCLIApp:
    """
    Command-Line Interface application for the Todo application.
    Provides a menu-driven interface for users to manage their tasks.
    """

    def __init__(self):
        """
        Initialize the CLI application with a task service.
        """
        self.task_service = TaskService()
        self.running = True

    def display_menu(self):
        """
        Display the main menu options to the user.
        """
        print("\n" + "="*40)
        print("TODO CLI APPLICATION")
        print("="*40)
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Task Complete/Incomplete")
        print("6. Exit")
        print("-"*40)

    def get_user_choice(self) -> str:
        """
        Get and validate user's menu choice.

        Returns:
            str: User's menu choice
        """
        while True:
            try:
                choice = input("Enter your choice (1-6): ").strip()
                if choice in ["1", "2", "3", "4", "5", "6"]:
                    return choice
                else:
                    print("Invalid choice. Please enter a number between 1 and 6.")
            except (EOFError, KeyboardInterrupt):
                print("\nExiting application...")
                return "6"  # Return exit choice

    def add_task(self):
        """
        Handle the add task functionality.
        Capture user input for title and description and add the task.
        """
        print("\n--- Add New Task ---")

        try:
            title = input("Enter task title: ").strip()
            if not title:
                print("Error: Title is required.")
                return

            description = input("Enter task description (optional, press Enter to skip): ").strip()

            result = self.task_service.add_task(title, description)

            if result["success"]:
                print(f"✓ {result['message']}")
            else:
                print(f"✗ Error: {result['message']}")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")

    def view_tasks(self):
        """
        Handle the view tasks functionality.
        Display all tasks with their details.
        """
        print("\n--- View All Tasks ---")

        tasks = self.task_service.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print(f"Total tasks: {len(tasks)}")
        print("-" * 50)

        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"[{status}] ID: {task.id} | Title: {task.title}")
            if task.description:
                print(f"    Description: {task.description}")
            print()

    def update_task(self):
        """
        Handle the update task functionality.
        Capture user input for task ID and new values.
        """
        print("\n--- Update Task ---")

        try:
            if not self.task_service.get_all_tasks():
                print("No tasks available to update.")
                return

            task_id_input = input("Enter task ID to update: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_input)
            task = self.task_service.get_task_by_id(task_id)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"Current task: {task}")

            new_title = input(f"Enter new title (current: '{task.title}', press Enter to keep current): ").strip()
            new_description = input(f"Enter new description (current: '{task.description}', press Enter to keep current): ").strip()

            # Prepare update parameters
            title_param = new_title if new_title else None
            description_param = new_description if new_description else None

            # If no changes were made, return early
            if title_param is None and description_param is None:
                print("No changes made.")
                return

            result = self.task_service.update_task(task_id, title_param, description_param)

            if result["success"]:
                print(f"✓ {result['message']}")
            else:
                print(f"✗ Error: {result['message']}")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")

    def delete_task(self):
        """
        Handle the delete task functionality.
        Capture user input for task ID and delete the task.
        """
        print("\n--- Delete Task ---")

        try:
            if not self.task_service.get_all_tasks():
                print("No tasks available to delete.")
                return

            task_id_input = input("Enter task ID to delete: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_input)
            task = self.task_service.get_task_by_id(task_id)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"Task to delete: {task}")
            confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()

            if confirm in ['y', 'yes']:
                result = self.task_service.delete_task(task_id)

                if result["success"]:
                    print(f"✓ {result['message']}")
                else:
                    print(f"✗ Error: {result['message']}")
            else:
                print("Deletion cancelled.")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")

    def toggle_task_completion(self):
        """
        Handle the toggle task completion functionality.
        Capture user input for task ID and toggle the completion status.
        """
        print("\n--- Mark Task Complete/Incomplete ---")

        try:
            if not self.task_service.get_all_tasks():
                print("No tasks available.")
                return

            task_id_input = input("Enter task ID to toggle: ").strip()
            if not task_id_input.isdigit():
                print("Error: Task ID must be a number.")
                return

            task_id = int(task_id_input)
            task = self.task_service.get_task_by_id(task_id)
            if not task:
                print(f"Error: Task with ID {task_id} not found.")
                return

            print(f"Current task: {task}")

            result = self.task_service.toggle_task_completion(task_id)

            if result["success"]:
                print(f"✓ {result['message']}")
            else:
                print(f"✗ Error: {result['message']}")
        except (EOFError, KeyboardInterrupt):
            print("\nOperation cancelled.")

    def run(self):
        """
        Main application loop that displays the menu and handles user choices.
        """
        print("Welcome to the Todo CLI Application!")

        while self.running:
            self.display_menu()
            choice = self.get_user_choice()

            if choice == "1":
                self.add_task()
            elif choice == "2":
                self.view_tasks()
            elif choice == "3":
                self.update_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.toggle_task_completion()
            elif choice == "6":
                print("\nThank you for using the Todo CLI Application!")
                print("Goodbye!")
                self.running = False

    def exit_app(self):
        """
        Set the running flag to False to exit the application.
        """
        self.running = False