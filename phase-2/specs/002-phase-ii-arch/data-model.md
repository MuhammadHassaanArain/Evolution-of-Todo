# Data Model: Phase II Architecture Foundation

## Overview
This document defines the data models required for the Phase II architecture, based on the entities identified in the feature specification.

## User Entity
**Purpose**: Represents an authenticated user in the system

**Fields**:
- `id` (UUID/String): Unique identifier for the user
- `email` (String): User's email address (unique, required)
- `name` (String): User's display name (optional)
- `hashed_password` (String): BCrypt hashed password
- `created_at` (DateTime): Account creation timestamp
- `updated_at` (DateTime): Last update timestamp
- `is_active` (Boolean): Account active status

**Validation Rules**:
- Email must be valid email format
- Email must be unique across all users
- Password must meet minimum security requirements
- User ID must be unique and immutable

**Relationships**:
- One-to-Many: User has many Tasks

## Task Entity
**Purpose**: Represents a user's task with CRUD operations

**Fields**:
- `id` (UUID/String): Unique identifier for the task
- `title` (String): Task title (required, max 200 characters)
- `description` (String): Task description (optional, max 1000 characters)
- `is_completed` (Boolean): Completion status (default: false)
- `user_id` (UUID/String): Foreign key to User
- `created_at` (DateTime): Task creation timestamp
- `updated_at` (DateTime): Last update timestamp

**Validation Rules**:
- Title must not be empty
- User ID must reference an existing user
- Only the owning user can modify the task
- Task cannot be modified by non-owning users

**Relationships**:
- Many-to-One: Task belongs to one User

## JWT Token Model
**Purpose**: Represents the structure of JWT tokens issued by the system

**Payload Fields**:
- `sub` (String): Subject (user ID)
- `iat` (Integer): Issued at timestamp (Unix time)
- `exp` (Integer): Expiration timestamp (Unix time)
- `jti` (String): JWT ID for potential revocation (optional)

**Validation Rules**:
- Token must not be expired at time of validation
- Token signature must be valid
- User referenced in token must exist and be active

## Session/Authentication Context
**Purpose**: Represents the authentication state for API requests

**Fields**:
- `user_id` (UUID/String): Authenticated user ID
- `token_scopes` (List): Permissions granted by token
- `authenticated_at` (DateTime): Time of authentication

## Database Relationships

```
User (1) -----> (Many) Task
```

- Foreign Key: Task.user_id references User.id
- Cascade: When User is deleted, associated Tasks are also deleted
- Constraints: All Tasks must have a valid owning User

## State Transitions

### Task State Transitions
- `is_completed: false` -> `is_completed: true` (Mark Complete)
- `is_completed: true` -> `is_completed: false` (Mark Incomplete)

### User State Transitions
- `is_active: true` -> `is_active: false` (Deactivate)
- `is_active: false` -> `is_active: true` (Reactivate)

## Security Considerations
- All user data is isolated by user_id
- Foreign key constraints prevent orphaned tasks
- Access control enforced at application layer
- No direct database access from frontend