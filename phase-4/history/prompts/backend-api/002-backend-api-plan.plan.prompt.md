---
id: 002
title: Backend API Plan
stage: plan
date: 2026-01-03
surface: agent
model: claude-sonnet-4-5-20250929
feature: backend-api
branch: 001-backend-api
user: Claude Code User
command: /sp.plan
labels: [api, backend, todos, authentication, authorization]
links:
  spec: specs/001-backend-api/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-backend-api/plan.md
 - specs/001-backend-api/research.md
 - specs/001-backend-api/data-model.md
 - specs/001-backend-api/quickstart.md
 - specs/001-backend-api/contracts/api-contracts.md
 - CLAUDE.md
tests:
 - null
---

## Prompt

```text
$ARGUMENTS
```

## Response snapshot

# Implementation Plan: Backend API (Business Logic)

**Branch**: `001-backend-api` | **Date**: 2026-01-03 | **Spec**: [link](specs/001-backend-api/spec.md)
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a secure, user-scoped REST API for Todo management with JWT-based authentication and ownership enforcement. The API will provide CRUD endpoints for todo management with proper authorization checks to ensure users can only access their own todos.

## Technical Context

**Language/Version**: Python 3.13+ (as required by constitution)
**Primary Dependencies**: FastAPI, JWT libraries (python-jose, passlib), Better Auth framework, SQLModel ORM
**Storage**: Neon Serverless PostgreSQL (as required by constitution)
**Testing**: pytest (standard Python testing framework)
**Target Platform**: Backend server environment
**Project Type**: Backend API service
**Performance Goals**: Efficient API responses with proper authentication and authorization checks
**Constraints**: Must enforce JWT-based authentication, ensure data isolation between users, follow RESTful principles
**Scale/Scope**: Multi-user environment with secure, isolated data access

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ **Spec-Driven Development**: Implementation based on written spec in `/specs/001-backend-api/spec.md`
- ✅ **No Manual Coding**: All code generated via Claude Code from specifications
- ✅ **Security & User Isolation**: API enforces JWT authentication and user ownership
- ✅ **Backend Standards**: Uses FastAPI for API endpoints as required
- ✅ **Authentication Requirements**: Uses JWT for authentication as required
- ✅ **Specification Rules**: API endpoints follow specifications exactly
- ✅ **Backend Standards**: Task ownership enforced on backend for every operation

## Project Structure

### Documentation (this feature)

```text
specs/001-backend-api/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py
│   │   ├── todos.py
│   │   └── auth.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── todo_service.py
│   │   └── auth_service.py
│   └── schemas/
│       ├── __init__.py
│       ├── todo.py
│       └── auth.py
└── tests/
    ├── unit/
    ├── integration/
    └── contract/
```

**Structure Decision**: Backend monorepo structure with dedicated API, models, services, and schemas directories following FastAPI best practices and constitution requirements for SQLModel ORM and JWT authentication.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|

# Research: Backend API (Business Logic)

## Decision: FastAPI Framework for Backend API
**Rationale**: Following the constitution requirement to use FastAPI for the backend API. FastAPI provides excellent support for JWT authentication, automatic OpenAPI documentation, and async capabilities which are well-suited for a todo management API.

**Alternatives considered**:
- Flask (rejected - FastAPI provides better automatic documentation and performance)
- Django (rejected - overkill for this API-focused application)
- Express.js (rejected - constitution specifies Python with FastAPI)

## Decision: JWT Authentication Implementation
**Rationale**: Following the specification requirement and constitution mandate to use JWT for authentication. JWT tokens will be validated on every request to ensure proper user ownership enforcement.

**Alternatives considered**:
- Session-based authentication (rejected - JWT is stateless and better for API scalability)
- OAuth2 (rejected - JWT with Better Auth is sufficient for this use case)
- API keys (rejected - JWT provides user context needed for ownership checks)

## Decision: Todo Ownership Enforcement Strategy
**Rationale**: Ownership will be enforced server-side on every request by checking the JWT token to identify the user and then verifying that any todo being accessed belongs to that user. This prevents cross-user data exposure.

**Alternatives considered**:
- Client-side ownership enforcement (rejected - security risk, client cannot be trusted)
- Database-level enforcement only (rejected - need application-level checks for complete security)
- Caching ownership information (rejected - adds complexity, direct validation preferred)

## Decision: Error Response Format
**Rationale**: Following REST API best practices with consistent error response format. All errors will return appropriate HTTP status codes with descriptive error messages in JSON format.

**Alternatives considered**:
- Different error formats (rejected - standard JSON format is expected by clients)
- Plain text errors (rejected - JSON is more structured and machine-readable)

## Decision: Request/Response Schema Validation
**Rationale**: Using Pydantic models for request/response validation to ensure data integrity and provide automatic documentation. This follows FastAPI's native capabilities.

**Alternatives considered**:
- Manual validation (rejected - Pydantic provides better validation and documentation)
- Different validation libraries (rejected - Pydantic is standard with FastAPI)
- No validation (rejected - security and data integrity requirements mandate validation)

## Decision: API Endpoint Structure
**Rationale**: Following RESTful principles with endpoints like `/todos` for collections and `/todos/{id}` for individual resources. This provides a clean, predictable API structure.

**Alternatives considered**:
- RPC-style endpoints (rejected - RESTful is more standard and discoverable)
- Different URL patterns (rejected - standard REST patterns are well-understood)

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

# Quickstart: Backend API (Business Logic)

## API Setup

1. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn python-jose[cryptography] passlib[bcrypt] python-multipart
   ```

2. **Environment Configuration**
   Set up required environment variables:
   ```bash
   export SECRET_KEY="your-secret-key-here"
   export ALGORITHM="HS256"
   export ACCESS_TOKEN_EXPIRE_MINUTES=30
   export DATABASE_URL="postgresql://user:password@localhost:5432/todo_app"
   ```

## API Usage Examples

### Authentication
All endpoints require a valid JWT token in the Authorization header:

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     http://localhost:8000/api/v1/todos
```

### Create a Todo
```bash
curl -X POST http://localhost:8000/api/v1/todos \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Buy groceries",
       "description": "Milk, bread, eggs",
       "is_completed": false
     }'
```

### List Todos
```bash
curl -X GET http://localhost:8000/api/v1/todos \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Get a Specific Todo
```bash
curl -X GET http://localhost:8000/api/v1/todos/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Update a Todo
```bash
curl -X PUT http://localhost:8000/api/v1/todos/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Buy Groceries (updated)",
       "is_completed": true
     }'
```

### Delete a Todo
```bash
curl -X DELETE http://localhost:8000/api/v1/todos/1 \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Key Features

- **JWT Authentication**: All endpoints require a valid JWT token
- **User Isolation**: Users can only access their own todos
- **Ownership Validation**: Server-side checks ensure proper authorization
- **RESTful Design**: Standard HTTP methods and status codes
- **Error Handling**: Consistent error response format
- **Input Validation**: Request schema validation with Pydantic
- **OpenAPI Documentation**: Auto-generated API documentation at `/docs`

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful GET/PUT requests
- `201 Created`: Successful POST requests
- `204 No Content`: Successful DELETE requests
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT
- `404 Not Found`: Resource doesn't exist or not owned by user
- `500 Internal Server Error`: Unexpected server errors

## Security

- JWT tokens are validated on every request
- User ownership is verified for each operation
- No cross-user data exposure is possible
- Request bodies are validated against schemas
- Sensitive internal identifiers are not exposed in responses

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

## Outcome

- ✅ Impact: Created comprehensive backend API implementation plan with JWT authentication and user ownership
- 🧪 Tests: Plan includes research, data model, contracts, and quickstart documentation
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, contracts/api-contracts.md
- 🔁 Next prompts: Ready for task generation phase
- 🧠 Reflection: Plan addresses all constitution requirements and establishes secure API foundation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A