# Data Model: Validation & Hardening

## Overview
This document defines the data models and validation rules for the validation and hardening feature, focusing on authentication tokens, user identification, and validation parameters.

## Authentication Token Model

### JWT Token Structure
```
{
  "sub": "user_id",           // Subject (user identifier)
  "exp": 1234567890,          // Expiration timestamp
  "iat": 1234567800,          // Issued at timestamp
  "jti": "token_id"           // JWT ID for token tracking (optional)
}
```

**Validation Rules**:
- `exp` must be in the future (not expired)
- `sub` must correspond to a valid user ID
- Token signature must be valid
- `iat` (issued at) should not be too far in the past (optional for token replay protection)

## User Model (with validation constraints)

### User Entity
- `id`: UUID (primary key, immutable)
- `email`: String (unique, valid email format)
- `created_at`: DateTime (auto-generated, immutable)
- `updated_at`: DateTime (auto-generated, updated on modification)

**Validation Rules**:
- User ID must exist in database before authentication
- Email format must be valid
- User must be active (not suspended/deleted)

## Todo Model (with ownership validation)

### Todo Entity
- `id`: UUID (primary key, immutable)
- `user_id`: UUID (foreign key to User, immutable after creation)
- `title`: String (max 255 characters, required)
- `description`: String (max 1000 characters, optional)
- `completed`: Boolean (default: false)
- `created_at`: DateTime (auto-generated, immutable)
- `updated_at`: DateTime (auto-generated, updated on modification)

**Validation Rules**:
- `user_id` must match the authenticated user for all operations
- `title` must not be empty
- `title` and `description` must be properly sanitized
- `completed` field must be boolean type

## API Request Models

### Validation for Todo Creation
- `title`: String (required, 1-255 characters)
- `description`: String (optional, 0-1000 characters)

**Validation Rules**:
- `title` must be present and non-empty
- `title` and `description` must not contain dangerous characters
- No `user_id` field allowed in payload (enforced by ownership)
- All unexpected fields should be rejected

### Validation for Todo Update
- `title`: String (optional, 1-255 characters)
- `description`: String (optional, 0-1000 characters)
- `completed`: Boolean (optional)

**Validation Rules**:
- No `user_id` field allowed in payload
- `title` must not exceed 255 characters if provided
- `description` must not exceed 1000 characters if provided
- `completed` must be boolean type if provided
- All unexpected fields should be rejected

## Error Response Model

### Standard Error Response
```
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": { ... } // optional, implementation-specific
  }
}
```

**Validation Rules**:
- Error responses must never expose internal system details
- Status codes must be appropriate for the error type (401, 403, 404, 400, 500)
- Error messages should be informative but not revealing of internal state

## Validation Parameters

### Token Validation Parameters
- `JWT_SECRET_KEY`: Secret key for JWT signing/verification
- `JWT_ALGORITHM`: Algorithm used for signing (default: "HS256")
- `JWT_EXPIRATION_MINUTES`: Token expiration duration (default: 15 minutes for access tokens)

### Request Validation Parameters
- `MAX_PAYLOAD_SIZE`: Maximum request payload size (default: 1MB)
- `MAX_TITLE_LENGTH`: Maximum length for todo title (255 characters)
- `MAX_DESCRIPTION_LENGTH`: Maximum length for todo description (1000 characters)

## State Transitions

### Todo State Transitions
- `pending` → `completed` (when `completed` field changes from false to true)
- `completed` → `pending` (when `completed` field changes from true to false)

**Validation Rules**:
- Only the owner of a todo can change its state
- State transitions must be validated against the authenticated user