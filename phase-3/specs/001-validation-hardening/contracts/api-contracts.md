# API Contract: Validation & Hardening

## Overview
This document defines the API contracts for validation and hardening measures in the todo application. These contracts ensure consistent validation behavior across all endpoints.

## Authentication Validation Contracts

### GET /todos/ (List Todos)
- **Authentication Required**: Yes
- **Authorization**: User can only access their own todos
- **Response Codes**:
  - `200 OK`: Successfully retrieved user's todos
  - `401 Unauthorized`: Invalid or missing authentication token
- **Validation**:
  - JWT token must be valid and unexpired
  - User ID from token must match requested resources

### GET /todos/{id} (Get Todo)
- **Authentication Required**: Yes
- **Authorization**: User can only access their own todo
- **Response Codes**:
  - `200 OK`: Successfully retrieved todo
  - `401 Unauthorized`: Invalid or missing authentication token
  - `404 Not Found`: Todo doesn't exist OR doesn't belong to user
- **Validation**:
  - JWT token must be valid and unexpired
  - Todo must belong to authenticated user (return 404 if not)

### POST /todos/ (Create Todo)
- **Authentication Required**: Yes
- **Authorization**: User can only create todos for themselves
- **Request Body**:
  - `title`: String, 1-255 characters (required)
  - `description`: String, 0-1000 characters (optional)
  - `completed`: Boolean (optional, default: false)
  - **Forbidden**: `user_id` field in payload
- **Response Codes**:
  - `201 Created`: Todo successfully created
  - `400 Bad Request`: Invalid request payload
  - `401 Unauthorized`: Invalid or missing authentication token
- **Validation**:
  - JWT token must be valid and unexpired
  - Request payload must not contain `user_id`
  - Request payload must not contain unexpected fields
  - Title must be 1-255 characters
  - Description must not exceed 1000 characters
  - Completed field must be boolean if provided

### PUT /todos/{id} (Update Todo)
- **Authentication Required**: Yes
- **Authorization**: User can only update their own todo
- **Request Body**:
  - `title`: String, 1-255 characters (optional)
  - `description`: String, 0-1000 characters (optional)
  - `completed`: Boolean (optional)
  - **Forbidden**: `user_id` field in payload
- **Response Codes**:
  - `200 OK`: Todo successfully updated
  - `400 Bad Request`: Invalid request payload
  - `401 Unauthorized`: Invalid or missing authentication token
  - `404 Not Found`: Todo doesn't exist OR doesn't belong to user
- **Validation**:
  - JWT token must be valid and unexpired
  - Todo must belong to authenticated user (return 404 if not)
  - Request payload must not contain `user_id`
  - Request payload must not contain unexpected fields
  - Title must be 1-255 characters if provided
  - Description must not exceed 1000 characters if provided
  - Completed field must be boolean if provided

### DELETE /todos/{id} (Delete Todo)
- **Authentication Required**: Yes
- **Authorization**: User can only delete their own todo
- **Response Codes**:
  - `204 No Content`: Todo successfully deleted
  - `401 Unauthorized`: Invalid or missing authentication token
  - `404 Not Found`: Todo doesn't exist OR doesn't belong to user
- **Validation**:
  - JWT token must be valid and unexpired
  - Todo must belong to authenticated user (return 404 if not)

## Error Response Format

All error responses follow the same format:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message"
  }
}
```

### Common Error Codes
- `AUTH_001`: "Invalid or expired token" (401)
- `AUTH_002`: "Missing authentication" (401)
- `VALIDATION_001`: "Invalid request payload" (400)
- `VALIDATION_002`: "Unexpected field in request" (400)
- `PERMISSION_001`: "Resource not found" (404) - for ownership violations
- `RESOURCE_001`: "Resource not found" (404) - for non-existent resources

## Validation Rules Summary

### Authentication Validation
- All user-specific endpoints require valid JWT token
- Expired tokens return 401 Unauthorized
- Malformed tokens return 401 Unauthorized
- Missing tokens return 401 Unauthorized

### Ownership Validation
- Users can only access their own resources
- Attempting to access another user's resource returns 404 Not Found
- No distinction is made between "doesn't exist" and "doesn't belong to you"

### Input Validation
- Requests with `user_id` in payload return 400 Bad Request
- Requests with unexpected fields return 400 Bad Request
- Requests with invalid data types return 400 Bad Request
- Oversized payloads return 400 Bad Request

## Security Requirements
- No internal system information exposed in error messages
- Stack traces never returned to clients
- Consistent error response format across all endpoints
- No information leakage about resource existence for unauthorized users