# API Contracts: Phase II Architecture Foundation

## Overview
This document defines the API contracts between frontend and backend as required by the specification. These contracts establish the HTTP contracts and OpenAPI schemas that enable proper separation between frontend and backend while maintaining clear communication.

## Authentication API Contracts

### POST /api/auth/login
**Purpose**: Authenticate user and issue JWT token

**Request**:
```
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "user_password"
}
```

**Response (200 OK)**:
```
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**Response (401 Unauthorized)**:
```
{
  "detail": "Invalid credentials"
}
```

### POST /api/auth/register
**Purpose**: Register new user and optionally return JWT token

**Request**:
```
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password",
  "name": "User Name"
}
```

**Response (201 Created)**:
```
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "user_id",
    "email": "user@example.com",
    "name": "User Name"
  }
}
```

**Response (400 Bad Request)**:
```
{
  "detail": "Email already registered"
}
```

### POST /api/auth/logout
**Purpose**: Logout user (server-side doesn't store sessions, but may implement token invalidation)

**Request**:
```
POST /api/auth/logout
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```
{
  "message": "Successfully logged out"
}
```

## Task API Contracts

### GET /api/tasks
**Purpose**: Retrieve all tasks for authenticated user

**Request**:
```
GET /api/tasks
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```
{
  "tasks": [
    {
      "id": "task_id_1",
      "title": "Task Title",
      "description": "Task Description",
      "is_completed": false,
      "user_id": "user_id",
      "created_at": "2023-01-01T00:00:00Z",
      "updated_at": "2023-01-01T00:00:00Z"
    }
  ]
}
```

**Response (401 Unauthorized)**:
```
{
  "detail": "Not authenticated"
}
```

### POST /api/tasks
**Purpose**: Create a new task for authenticated user

**Request**:
```
POST /api/tasks
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "New Task",
  "description": "Task Description"
}
```

**Response (201 Created)**:
```
{
  "id": "new_task_id",
  "title": "New Task",
  "description": "Task Description",
  "is_completed": false,
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

### GET /api/tasks/{task_id}
**Purpose**: Retrieve a specific task for authenticated user

**Request**:
```
GET /api/tasks/{task_id}
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```
{
  "id": "task_id",
  "title": "Task Title",
  "description": "Task Description",
  "is_completed": false,
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (404 Not Found)**:
```
{
  "detail": "Task not found"
}
```

**Response (403 Forbidden)**:
```
{
  "detail": "Access denied"
}
```

### PUT /api/tasks/{task_id}
**Purpose**: Update a specific task for authenticated user

**Request**:
```
PUT /api/tasks/{task_id}
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "title": "Updated Task Title",
  "description": "Updated Description",
  "is_completed": true
}
```

**Response (200 OK)**:
```
{
  "id": "task_id",
  "title": "Updated Task Title",
  "description": "Updated Description",
  "is_completed": true,
  "user_id": "user_id",
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

### DELETE /api/tasks/{task_id}
**Purpose**: Delete a specific task for authenticated user

**Request**:
```
DELETE /api/tasks/{task_id}
Authorization: Bearer {access_token}
```

**Response (204 No Content)**:

**Response (404 Not Found)**:
```
{
  "detail": "Task not found"
}
```

## Error Response Format

All error responses follow the same format:
```
{
  "detail": "Error message explaining the issue"
}
```

## Authorization Headers
All protected endpoints require the Authorization header:
```
Authorization: Bearer {jwt_token}
```

## Security Requirements
- All protected endpoints validate JWT tokens
- User isolation enforced: users can only access their own resources
- Invalid/missing tokens result in 401 Unauthorized
- Valid token but unauthorized access results in 403 Forbidden