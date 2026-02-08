# API Contracts: Backend API (Business Logic)

## OpenAPI Specification for Todo API

### Base Path: `/api/v1` (assumed)

### Security Scheme
```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Schemas

#### Todo Object
```json
{
  "type": "object",
  "required": ["id", "title", "is_completed", "created_at", "updated_at"],
  "properties": {
    "id": {
      "type": "integer",
      "description": "Unique identifier for the todo",
      "example": 1
    },
    "title": {
      "type": "string",
      "description": "Title of the todo item",
      "example": "Buy groceries"
    },
    "description": {
      "type": "string",
      "description": "Optional description of the todo",
      "example": "Milk, bread, eggs",
      "nullable": true
    },
    "is_completed": {
      "type": "boolean",
      "description": "Whether the todo is completed",
      "example": false
    },
    "created_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp when todo was created",
      "example": "2023-01-01T12:00:00Z"
    },
    "updated_at": {
      "type": "string",
      "format": "date-time",
      "description": "Timestamp when todo was last updated",
      "example": "2023-01-01T12:00:00Z"
    }
  }
}
```

#### Todo Creation Request
```json
{
  "type": "object",
  "required": ["title"],
  "properties": {
    "title": {
      "type": "string",
      "description": "Title of the todo item",
      "example": "Buy groceries"
    },
    "description": {
      "type": "string",
      "description": "Optional description of the todo",
      "example": "Milk, bread, eggs",
      "nullable": true
    },
    "is_completed": {
      "type": "boolean",
      "description": "Whether the todo is completed",
      "default": false
    }
  }
}
```

#### Todo Update Request
```json
{
  "type": "object",
  "properties": {
    "title": {
      "type": "string",
      "description": "Updated title of the todo item",
      "example": "Buy groceries"
    },
    "description": {
      "type": "string",
      "description": "Updated description of the todo",
      "example": "Milk, bread, eggs",
      "nullable": true
    },
    "is_completed": {
      "type": "boolean",
      "description": "Updated completion status",
      "example": true
    }
  }
}
```

### Endpoints

#### POST /todos
**Summary**: Create a new todo
**Description**: Creates a new todo for the authenticated user. The owner is derived from the JWT token.
**Security**: Bearer token required
**Request Body**:
- Content-Type: application/json
- Schema: Todo Creation Request
**Responses**:
- 201 Created: Todo created successfully
  - Content-Type: application/json
  - Schema: Todo Object
- 400 Bad Request: Invalid request body
- 401 Unauthorized: Invalid or missing JWT
- 500 Internal Server Error: Unexpected error

#### GET /todos
**Summary**: List user's todos
**Description**: Returns all todos owned by the authenticated user.
**Security**: Bearer token required
**Responses**:
- 200 OK: Todos retrieved successfully
  - Content-Type: application/json
  - Schema: Array of Todo Objects
- 401 Unauthorized: Invalid or missing JWT
- 500 Internal Server Error: Unexpected error

#### GET /todos/{id}
**Summary**: Get a specific todo
**Description**: Returns a specific todo if it's owned by the authenticated user.
**Security**: Bearer token required
**Path Parameters**:
- id (integer, required): The ID of the todo to retrieve
**Responses**:
- 200 OK: Todo retrieved successfully
  - Content-Type: application/json
  - Schema: Todo Object
- 401 Unauthorized: Invalid or missing JWT
- 404 Not Found: Todo doesn't exist or isn't owned by user
- 500 Internal Server Error: Unexpected error

#### PUT /todos/{id}
**Summary**: Update a specific todo
**Description**: Updates a specific todo if it's owned by the authenticated user.
**Security**: Bearer token required
**Path Parameters**:
- id (integer, required): The ID of the todo to update
**Request Body**:
- Content-Type: application/json
- Schema: Todo Update Request
**Responses**:
- 200 OK: Todo updated successfully
  - Content-Type: application/json
  - Schema: Todo Object
- 400 Bad Request: Invalid request body
- 401 Unauthorized: Invalid or missing JWT
- 404 Not Found: Todo doesn't exist or isn't owned by user
- 500 Internal Server Error: Unexpected error

#### DELETE /todos/{id}
**Summary**: Delete a specific todo
**Description**: Deletes a specific todo if it's owned by the authenticated user.
**Security**: Bearer token required
**Path Parameters**:
- id (integer, required): The ID of the todo to delete
**Responses**:
- 204 No Content: Todo deleted successfully
- 401 Unauthorized: Invalid or missing JWT
- 404 Not Found: Todo doesn't exist or isn't owned by user
- 500 Internal Server Error: Unexpected error

### Error Response Format
```json
{
  "detail": {
    "type": "string",
    "description": "Human-readable error message",
    "example": "Todo not found or not owned by user"
  },
  "error_code": {
    "type": "string",
    "description": "Machine-readable error code",
    "example": "TODO_NOT_FOUND",
    "nullable": true
  },
  "timestamp": {
    "type": "string",
    "format": "date-time",
    "description": "Timestamp when the error occurred",
    "example": "2023-01-01T12:00:00Z"
  }
}
```

### Common Headers
- Authorization: Bearer {JWT_TOKEN} (for authenticated endpoints)
- Content-Type: application/json (for request bodies)
- Accept: application/json (for response bodies)

### Error Codes
- `UNAUTHORIZED`: 401 - Invalid or missing JWT
- `TODO_NOT_FOUND`: 404 - Todo doesn't exist or isn't owned by user
- `BAD_REQUEST`: 400 - Invalid request body
- `INTERNAL_ERROR`: 500 - Unexpected server error