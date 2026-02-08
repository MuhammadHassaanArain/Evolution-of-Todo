# API Contracts: Frontend Data Access Layer

## Overview
This document specifies the API contracts for the frontend data access layer. It defines the interface between the frontend application and the backend API services.

## Base URL
All API endpoints are relative to:
`http://localhost:8000/api/v1` (development)
`https://api.todoapp.com/v1` (production)

## Authentication
All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt-token>
```

Public endpoints (like login, signup) do not require authentication.

## Common Response Format

### Success Responses
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional message"
}
```

### Error Responses
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": "Optional details"
  }
}
```

## Endpoints

### Public Endpoints (No Authentication Required)

#### POST /auth/login
**Description**: Authenticate user and return JWT token

Request:
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response (200):
```json
{
  "success": true,
  "data": {
    "access_token": "jwt-token-string",
    "token_type": "bearer",
    "expires_in": 1800
  }
}
```

#### POST /auth/register
**Description**: Register a new user account

Request:
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe"
}
```

Response (201):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe"
  }
}
```

### Protected Endpoints (Authentication Required)

#### GET /todos
**Description**: Get todos for authenticated user

Response (200):
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "title": "Todo title",
      "description": "Todo description",
      "is_completed": false,
      "owner_id": 1,
      "created_at": "2023-01-01T12:00:00Z",
      "updated_at": "2023-01-01T12:00:00Z"
    }
  ]
}
```

#### POST /todos
**Description**: Create a new todo for authenticated user

Request:
```json
{
  "title": "New todo",
  "description": "Todo description",
  "is_completed": false
}
```

Response (201):
```json
{
  "success": true,
  "data": {
    "id": 2,
    "title": "New todo",
    "description": "Todo description",
    "is_completed": false,
    "owner_id": 1,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  }
}
```

#### GET /todos/{id}
**Description**: Get a specific todo by ID if owned by user

Response (200):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Todo title",
    "description": "Todo description",
    "is_completed": false,
    "owner_id": 1,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-01T12:00:00Z"
  }
}
```

#### PUT /todos/{id}
**Description**: Update a specific todo if owned by user

Request:
```json
{
  "title": "Updated title",
  "description": "Updated description",
  "is_completed": true
}
```

Response (200):
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Updated title",
    "description": "Updated description",
    "is_completed": true,
    "owner_id": 1,
    "created_at": "2023-01-01T12:00:00Z",
    "updated_at": "2023-01-02T10:00:00Z"
  }
}
```

#### DELETE /todos/{id}
**Description**: Delete a specific todo if owned by user

Response (204):
```
Status: 204 No Content
```

## Error Response Codes

- `400 Bad Request`: Invalid request format or validation errors
- `401 Unauthorized`: Missing or invalid JWT token
- `403 Forbidden`: Valid token but insufficient permissions
- `404 Not Found`: Resource does not exist or not owned by user
- `422 Unprocessable Entity`: Validation errors in request body
- `500 Internal Server Error`: Server-side error occurred

## Data Models

### User Model
```typescript
interface User {
  id: number;
  email: string;
  username: string;
  first_name?: string;
  last_name?: string;
  is_active: boolean;
  created_at: string; // ISO 8601 date string
  updated_at: string; // ISO 8601 date string
}
```

### Todo Model
```typescript
interface Todo {
  id: number;
  title: string;
  description?: string;
  is_completed: boolean;
  owner_id: number;
  created_at: string; // ISO 8601 date string
  updated_at: string; // ISO 8601 date string
}
```

## Security Considerations

- JWT tokens must be securely stored and transmitted
- Sensitive data must not be logged
- API endpoints should implement rate limiting
- Input validation must be performed on all request parameters
- All responses should sanitize sensitive information