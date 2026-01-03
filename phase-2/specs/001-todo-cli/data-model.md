# Data Model: Todo CLI Application

## Entity: Task

**Attributes:**
- `id`: integer (unique identifier, required)
- `title`: string (task title, required)
- `description`: string (task description, optional, default: "")
- `completed`: boolean (completion status, required, default: False)

**Validation Rules:**
- `id` must be unique within the task collection
- `title` must not be empty or null
- `completed` must be a boolean value

**State Transitions:**
- `completed = False` → `completed = True` (when marking as complete)
- `completed = True` → `completed = False` (when marking as incomplete)

## Entity: TaskList (Collection)

**Attributes:**
- `tasks`: list of Task objects (in-memory storage)

**Operations:**
- Add task to list
- Remove task from list by ID
- Update task by ID
- Retrieve all tasks
- Find task by ID

**Constraints:**
- All tasks must have unique IDs
- In-memory only (no persistence)