# API Contracts: Authentication Service

## Overview
This document defines the API contracts for the authentication service in the full-stack todo web application. These contracts specify the endpoints, request/response formats, and error handling for the JWT-based authentication system.

## Base URL
```
http://localhost:8000/api/v1 (development)
https://yourdomain.com/api/v1 (production)
```

## Authentication Endpoints

### 1. User Registration
**Endpoint**: `POST /auth/register`

**Description**: Creates a new user account and returns an authentication token.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "string (required, valid email format)",
  "password": "string (required, minimum 8 characters)",
  "first_name": "string (optional)",
  "last_name": "string (optional)"
}
```

**Success Response (200 OK)**:
```json
{
  "access_token": "string (JWT token)",
  "token_type": "string (typically 'bearer')"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input data
  ```json
  {
    "detail": "Email already registered"
  }
  ```
- `422 Unprocessable Entity`: Validation error
  ```json
  {
    "detail": [
      {
        "loc": ["body", "email"],
        "msg": "value is not a valid email address",
        "type": "value_error.email"
      }
    ]
  }
  ```

### 2. User Login
**Endpoint**: `POST /auth/login`

**Description**: Authenticates a user with email and password, returns an authentication token.

**Request Headers**:
```
Content-Type: application/json
```

**Request Body**:
```json
{
  "email": "string (required, valid email format)",
  "password": "string (required)"
}
```

**Success Response (200 OK)**:
```json
{
  "access_token": "string (JWT token)",
  "token_type": "string (typically 'bearer')"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid credentials
  ```json
  {
    "detail": "Incorrect email or password"
  }
  ```
- `422 Unprocessable Entity`: Validation error
  ```json
  {
    "detail": [
      {
        "loc": ["body", "email"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
  ```

### 3. Get Current User
**Endpoint**: `GET /auth/me`

**Description**: Returns the authenticated user's information.

**Request Headers**:
```
Authorization: Bearer <token> (required)
```

**Success Response (200 OK)**:
```json
{
  "id": "string (user UUID)",
  "email": "string (user email)",
  "first_name": "string (optional)",
  "last_name": "string (optional)",
  "created_at": "datetime (ISO 8601 format)",
  "updated_at": "datetime (ISO 8601 format)",
  "is_active": "boolean",
  "email_verified": "boolean"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

### 4. User Logout
**Endpoint**: `POST /auth/logout`

**Description**: Performs logout (in stateless JWT system, primarily for client-side cleanup).

**Request Headers**:
```
Authorization: Bearer <token> (required)
```

**Success Response (200 OK)**:
```json
{
  "message": "Successfully logged out"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid or missing token
  ```json
  {
    "detail": "Not authenticated"
  }
  ```

## Common Error Responses

### 401 Unauthorized
**Description**: Request requires authentication or provided token is invalid.

**Response Body**:
```json
{
  "detail": "Not authenticated"
}
```

### 422 Unprocessable Entity
**Description**: Request validation failed.

**Response Body**:
```json
{
  "detail": [
    {
      "loc": ["string", "field_location"],
      "msg": "error_message",
      "type": "error_type"
    }
  ]
}
```

### 500 Internal Server Error
**Description**: Unexpected server error occurred.

**Response Body**:
```json
{
  "detail": "Internal server error"
}
```

## JWT Token Format

### Access Token Structure
```
Header.Payload.Signature
```

### Header
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

### Payload Claims
```json
{
  "sub": "user_id_string",
  "email": "user@example.com",
  "exp": 1234567890,
  "iat": 1234567800,
  "type": "access"
}
```

**Claims**:
- `sub`: Subject (user ID)
- `email`: User email
- `exp`: Expiration timestamp (Unix timestamp)
- `iat`: Issued at timestamp (Unix timestamp)
- `type`: Token type (access)

## Authentication Flow Contracts

### Registration Flow
1. Client sends `POST /auth/register` with user credentials
2. Server validates input and creates user record
3. Server generates JWT access token
4. Server returns token in response

### Login Flow
1. Client sends `POST /auth/login` with credentials
2. Server validates credentials against stored hash
3. Server generates JWT access token
4. Server returns token in response

### Protected Resource Access
1. Client includes `Authorization: Bearer <token>` header
2. Server validates token signature and expiration
3. Server extracts user identity from token
4. Server processes request with user context

## Security Requirements

### Token Validation
- All protected endpoints must validate JWT tokens
- Token must not be expired
- Token signature must be valid
- Token must contain valid user ID

### Password Requirements
- Minimum 8 characters
- Should contain uppercase, lowercase, number, and special character
- Must be hashed using bcrypt with minimum work factor of 12

### Rate Limiting
- Authentication endpoints should implement rate limiting
- Recommended: 5 attempts per IP per 15 minutes

## Versioning
- API version is included in URL path: `/api/v1/`
- Breaking changes require new version number
- Non-breaking changes can be made within same version

## Content Types
- All requests must use `application/json` content type
- All responses return `application/json` content type
- Error responses follow RFC 7807 Problem Details specification

## Client Implementation Guidelines

### Token Storage
- Store JWT tokens securely on client-side
- Use HttpOnly cookies when possible for additional security
- Implement automatic token refresh if refresh tokens are available

### Error Handling
- Handle 401 responses by redirecting to login page
- Display validation errors to users in user-friendly format
- Implement retry logic for network errors

### Session Management
- Check token expiration before making requests
- Implement automatic logout when token expires
- Provide clear feedback to users about authentication status