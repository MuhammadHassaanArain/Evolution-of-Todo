# Data Model: MCP Server for Todo Task Management

## Entities

### Task
**Description**: Represents a user's todo item that can be managed through MCP tools

**Fields**:
- id (integer): Unique identifier for the task
- title (string): Title of the task (required)
- description (string): Optional description of the task
- completed (boolean): Whether the task is completed or not
- user_id (integer): Reference to the user who owns the task

**Validation Rules**:
- title must be provided for all operations
- id must be a positive integer for update, complete, and delete operations
- user_id is inherited from the authenticated user context

### User Context
**Description**: Represents the authenticated user whose tasks are being managed

**Fields**:
- user_id (integer): Unique identifier for the authenticated user
- jwt_token (string): Authentication token passed to backend

**Validation Rules**:
- user_id must match the authenticated user from the JWT token
- jwt_token must be valid and present for all operations

### MCP Tool Request
**Description**: Represents a request from an AI agent to perform a task operation

**Fields**:
- tool_name (string): Name of the MCP tool being called (add_task, list_tasks, update_task, complete_task, delete_task)
- parameters (object): Parameters specific to each tool
- auth_header (string): Authorization header containing JWT token

**Validation Rules**:
- tool_name must be one of the supported MCP tools
- parameters must match the expected schema for each tool
- auth_header must be present and valid

## State Transitions

### Task State Transitions
- Pending → Completed: When complete_task tool is called
- Completed → Pending: When update_task tool modifies the completed status to false

### MCP Tool Lifecycle
- Request received → Validation → Backend API call → Response preparation → Response sent to AI agent