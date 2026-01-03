# Todo CLI Application

A simple command-line interface (CLI) application for managing todo tasks. This application allows users to add, view, update, delete, and mark tasks as complete/incomplete through an interactive console interface.

## Features

- Add new tasks with title and optional description
- View all tasks with their completion status
- Update existing task details
- Delete tasks by ID
- Mark tasks as complete/incomplete
- In-memory storage (no persistence)

## Requirements

- Python 3.13+
- No external dependencies required

## Installation

1. Clone the repository
2. Ensure Python 3.12+ is installed
3. Install UV package manager: `pip install uv`
4. No external dependencies required (uses standard library only)

## Usage

Run the application using UV:

```bash
uv run main.py
```

Or run as a module:

```bash
uv run python -m src.main
```

Or install and run as a command:

```bash
uv tool install .
todo
```

The application will start an interactive menu where you can:
- Add a new task
- View all tasks
- Update task details
- Delete tasks
- Mark tasks as complete/incomplete
- Exit the application

## Project Structure

```
src/
├── todo/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task model definition
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # CRUD operations for tasks
│   └── cli/
│       ├── __init__.py
│       └── cli_app.py       # Console interface and menu system
├── __init__.py
└── main.py                 # Application entry point

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   └── test_task.py        # Unit tests for Task model
├── integration/
│   ├── __init__.py
│   └── test_task_service.py # Integration tests for task operations
└── __init__.py
```

## Architecture

The application follows a clean architecture pattern with:
- **Models**: Data representation and validation
- **Services**: Business logic and operations
- **CLI**: User interface and interaction