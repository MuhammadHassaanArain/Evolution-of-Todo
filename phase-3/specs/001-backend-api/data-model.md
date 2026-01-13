# Data Model: Backend API (Business Logic)

## Entity: Todo (API Schema)

**Request Schema - TodoCreate**
- `title` (str, non-nullable) - Title of the todo item
- `description` (str, nullable) - Optional description of the todo
- `is_completed` (bool, default=False) - Whether the todo is completed

**Request Schema - TodoUpdate**
- `title` (str, optional) - Updated title of the todo item
- `description` (str, optional) - Updated description of the todo
- `is_completed` (bool, optional) - Updated completion status

**Response Schema - TodoResponse**
- `id` (int) - Unique identifier for the todo
- `title` (str) - Title of the todo item
- `description` (str, nullable) - Description of the todo
- `is_completed` (bool) - Whether the todo is completed
- `created_at` (datetime) - Timestamp when todo was created
- `updated_at` (datetime) - Timestamp when todo was last updated
- `owner_id` (int) - ID of the user who owns this todo (internal field, not exposed in responses)

## Entity: JWT Token (Authentication)

**JWT Payload Structure**
- `sub` (str) - Subject (user ID)
- `exp` (int) - Expiration timestamp
- `iat` (int) - Issued at timestamp
- `jti` (str) - JWT ID for token management (optional)

## API Endpoints

### POST /todos
**Purpose**: Create a new todo for the authenticated user
**Authentication**: JWT required
**Request Body**: TodoCreate schema
**Response**: 201 Created with TodoResponse schema
**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT
- 400 Bad Request: Invalid request body

### GET /todos
**Purpose**: List all todos for the authenticated user
**Authentication**: JWT required
**Request Body**: None
**Response**: 200 OK with array of TodoResponse schemas
**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT

### GET /todos/{id}
**Purpose**: Get a specific todo by ID if owned by the user
**Authentication**: JWT required
**Request Body**: None
**Path Parameter**: id (int) - Todo ID
**Response**: 200 OK with TodoResponse schema
**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT
- 404 Not Found: Todo doesn't exist or isn't owned by user

### PUT /todos/{id}
**Purpose**: Update a specific todo if owned by the user
**Authentication**: JWT required
**Request Body**: TodoUpdate schema
**Path Parameter**: id (int) - Todo ID
**Response**: 200 OK with updated TodoResponse schema
**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT
- 404 Not Found: Todo doesn't exist or isn't owned by user
- 400 Bad Request: Invalid request body

### DELETE /todos/{id}
**Purpose**: Delete a specific todo if owned by the user
**Authentication**: JWT required
**Path Parameter**: id (int) - Todo ID
**Response**: 204 No Content
**Error Responses**:
- 401 Unauthorized: Invalid or missing JWT
- 404 Not Found: Todo doesn't exist or isn't owned by user

## Validation Rules

### Todo Creation
- Title must not be empty
- Title must be less than 255 characters
- Description must be less than 1000 characters if provided

### Todo Update
- If title is provided, it must not be empty
- If title is provided, it must be less than 255 characters
- If description is provided, it must be less than 1000 characters

### Ownership Validation
- All operations validate that the todo belongs to the authenticated user
- Non-existent or non-owned todos return 404 Not Found (no distinction)

## Error Response Format

### Standard Error Response
- `detail` (str) - Human-readable error message
- `error_code` (str, optional) - Machine-readable error code
- `timestamp` (datetime, optional) - When the error occurred

### Example Error Response
```json
{
  "detail": "Todo not found or not owned by user",
  "error_code": "TODO_NOT_FOUND"
}
```

## Authentication Requirements

### JWT Validation
- Token must be present in Authorization header as "Bearer {token}"
- Token must not be expired
- Token must be properly signed
- Token must contain valid user identifier

### Authorization Checks
- Before each operation, verify the authenticated user owns the requested resource
- Use the user ID from the JWT payload to validate ownership
- Deny access to resources not owned by the authenticated user