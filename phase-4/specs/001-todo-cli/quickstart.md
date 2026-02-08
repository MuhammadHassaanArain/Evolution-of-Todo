# Quickstart Guide: Todo CLI Application

## Prerequisites
- Python 3.13+ installed
- UV package manager (for dependency management)

## Setup
1. Clone the repository
2. Navigate to the project directory
3. Install dependencies: `uv sync` (or `pip install -r requirements.txt`)
4. Run the application: `python -m src.main`

## Usage
1. The application will display a menu with the following options:
   - 1. Add Task
   - 2. View Tasks
   - 3. Update Task
   - 4. Delete Task
   - 5. Mark Task Complete/Incomplete
   - 6. Exit

2. Follow the on-screen prompts to perform operations

## Development
- All source code is located in the `src/todo/` directory
- Models are in `src/todo/models/`
- Business logic is in `src/todo/services/`
- CLI interface is in `src/todo/cli/`
- Tests are in the `tests/` directory