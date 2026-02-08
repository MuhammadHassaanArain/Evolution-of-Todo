# API Reference: Todo Backend

## Overview

This document provides a comprehensive reference for the Todo backend API, which implements secure, user-scoped todo management with ownership enforcement at the database level.

## Authentication

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

Tokens are obtained through the authentication endpoints and are valid for 30 minutes by default.

## Base URL

All endpoints are prefixed with `/api/v1/`

## Common Response Formats

### Success Responses

Most successful operations return a JSON object with the relevant data.

### Error Responses

All error responses follow this format:

```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_ERROR_CODE",
  "timestamp": "ISO 8601 timestamp"
}
```

## Endpoints

### Todo Management

#### `POST /todos`

Create a new todo for the authenticated user.

**Request Body:**
```json
{
  "title": "string (required, 1-255 chars)",
  "description": "string (optional, max 1000 chars)",
  "is_completed": "boolean (optional, default: false)"
}
```

**Response (201 Created):**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "is_completed": "boolean",
  "owner_id": "integer",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

**Errors:**
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT
- `422 Unprocessable Entity`: Validation error

#### `GET /todos`

Retrieve all todos owned by the authenticated user.

**Query Parameters:**
- `skip` (integer, optional): Number of records to skip (default: 0)
- `limit` (integer, optional): Maximum number of records to return (default: 100)

**Response (200 OK):**
```json
[
  {
    "id": "integer",
    "title": "string",
    "description": "string or null",
    "is_completed": "boolean",
    "owner_id": "integer",
    "created_at": "ISO 8601 datetime",
    "updated_at": "ISO 8601 datetime"
  }
]
```

**Errors:**
- `401 Unauthorized`: Invalid or missing JWT

#### `GET /todos/{id}`

Retrieve a specific todo if owned by the authenticated user.

**Path Parameters:**
- `id` (integer): The ID of the todo to retrieve

**Response (200 OK):**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "is_completed": "boolean",
  "owner_id": "integer",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

**Errors:**
- `401 Unauthorized`: Invalid or missing JWT
- `404 Not Found`: Todo not found or not owned by user

#### `PUT /todos/{id}`

Update a specific todo if owned by the authenticated user.

**Path Parameters:**
- `id` (integer): The ID of the todo to update

**Request Body:**
```json
{
  "title": "string (optional, 1-255 chars)",
  "description": "string (optional, max 1000 chars)",
  "is_completed": "boolean (optional)"
}
```

**Response (200 OK):**
```json
{
  "id": "integer",
  "title": "string",
  "description": "string or null",
  "is_completed": "boolean",
  "owner_id": "integer",
  "created_at": "ISO 8601 datetime",
  "updated_at": "ISO 8601 datetime"
}
```

**Errors:**
- `400 Bad Request`: Invalid request body
- `401 Unauthorized`: Invalid or missing JWT
- `404 Not Found`: Todo not found or not owned by user
- `422 Unprocessable Entity`: Validation error

#### `DELETE /todos/{id}`

Delete a specific todo if owned by the authenticated user.

**Path Parameters:**
- `id` (integer): The ID of the todo to delete

**Response (204 No Content):**
No content returned.

**Errors:**
- `401 Unauthorized`: Invalid or missing JWT
- `404 Not Found`: Todo not found or not owned by user

## Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid authentication token |
| `FORBIDDEN` | 403 | User does not have permission to access resource |
| `NOT_FOUND` | 404 | Resource not found or not owned by user |
| `VALIDATION_ERROR` | 422 | Request body validation failed |
| `INTERNAL_ERROR` | 500 | An unexpected server error occurred |

## Data Models

### User
Represents an authenticated account in the system.
- `id`: Unique identifier
- `email`: User's email address (unique)
- `username`: User's chosen username (unique)
- `first_name`: User's first name (optional)
- `last_name`: User's last name (optional)
- `is_active`: Whether the account is active
- `created_at`: Timestamp when account was created
- `updated_at`: Timestamp when account was last updated

### Todo
Represents a task owned by a user.
- `id`: Unique identifier
- `title`: Title of the task (required)
- `description`: Detailed description of the task (optional)
- `is_completed`: Whether the task is completed
- `owner_id`: ID of the user who owns this todo
- `created_at`: Timestamp when todo was created
- `updated_at`: Timestamp when todo was last updated

## Security

- All data access is restricted to the authenticated user
- Ownership is enforced at the database level with foreign key constraints
- JWT tokens are validated on every request
- No cross-user data access is possible
- Passwords are hashed using bcrypt

## Database Schema

The database schema includes:
- A `users` table with user account information
- A `todos` table with todo items linked to users via foreign key
- Proper indexing for efficient user-scoped queries
- Referential integrity constraints to prevent orphaned data
