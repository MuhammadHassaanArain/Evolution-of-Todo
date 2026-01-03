# Data Model: Phase II — Chunk 1: Authentication (ISOLATED)

## Overview
This document defines the data models required for the JWT-based authentication system. The models focus on user identity and authentication data while maintaining isolation from domain logic.

## Entity Models

### User Model
**Purpose**: Represents authenticated users in the system

```python
# backend/src/models/user.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class User(UserBase, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    email_verified: bool = Field(default=False)

class UserRead(UserBase):
    id: str
    created_at: datetime
    updated_at: datetime
    is_active: bool
    email_verified: bool

class UserCreate(UserBase):
    password: str
    email: str

class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
```

**Fields**:
- `id`: Unique identifier for the user (UUID string)
- `email`: User's email address (unique, indexed)
- `password_hash`: Hashed password using bcrypt
- `first_name`, `last_name`: Optional user profile information
- `created_at`, `updated_at`: Timestamps for record management
- `is_active`: Boolean indicating if the account is active
- `email_verified`: Boolean indicating if email has been verified

**Constraints**:
- Email must be unique
- Email must be properly formatted
- Password must be hashed before storage
- User ID is auto-generated as UUID

### Token Model
**Purpose**: Represents JWT token information for validation and introspection

```python
# backend/src/models/auth.py
from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None
    email: Optional[str] = None

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict  # Contains user ID and basic info
```

**Fields**:
- `access_token`: JWT token string
- `token_type`: Token type (typically "bearer")
- `user_id`: User identifier from token claims
- `email`: User email from token claims
- `user`: Dictionary containing user information

## Request/Response Models

### Authentication Requests
```python
# backend/src/models/auth.py
class UserLogin(BaseModel):
    email: str
    password: str

class UserRegister(UserCreate):
    pass  # Extends UserCreate with same fields

class AuthMeResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    created_at: datetime
```

### Authentication Responses
```python
# backend/src/models/auth.py
class AuthSuccessResponse(BaseModel):
    success: bool
    message: str
    data: Token

class AuthErrorResponse(BaseModel):
    success: bool
    message: str
    error_code: str
```

## Database Schema

### Users Table
```
Table: users
- id: VARCHAR(36) PRIMARY KEY
- email: VARCHAR(255) UNIQUE NOT NULL INDEX
- password_hash: VARCHAR(255) NOT NULL
- first_name: VARCHAR(100) NULL
- last_name: VARCHAR(100) NULL
- created_at: TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
- updated_at: TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
- is_active: BOOLEAN NOT NULL DEFAULT TRUE
- email_verified: BOOLEAN NOT NULL DEFAULT FALSE
```

**Indexes**:
- Primary Key: id
- Unique: email
- Index: email (for lookup performance)

## JWT Payload Structure

### Token Claims
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
- `exp`: Expiration timestamp
- `iat`: Issued at timestamp
- `type`: Token type (access)

## Relationships

### User to Tasks (Future Reference)
**Note**: This relationship is defined for future integration but not implemented in this auth-only chunk.

- One User has many Tasks
- Tasks are filtered by user_id
- Access control enforced at the API layer

## Validation Rules

### User Model Validation
1. **Email Format**: Must be valid email format (using Pydantic validation)
2. **Email Uniqueness**: Email must not already exist in database
3. **Password Strength**: Minimum 8 characters (validation in service layer)
4. **Field Lengths**:
   - Email: max 255 characters
   - First name: max 100 characters
   - Last name: max 100 characters

### Token Validation
1. **Signature Verification**: JWT signature must be valid
2. **Expiration Check**: Token must not be expired
3. **Issuer Verification**: Token must be issued by our system
4. **Subject Validation**: User ID in token must exist in database

## API Data Flow

### Registration Flow
1. Client sends `UserRegister` data
2. Backend validates input
3. Password is hashed
4. User record is created
5. JWT token is generated
6. `AuthSuccessResponse` is returned

### Login Flow
1. Client sends `UserLogin` data
2. Backend validates credentials
3. JWT token is generated
4. `AuthSuccessResponse` is returned

### Auth Me Flow
1. Client sends JWT in Authorization header
2. Backend validates token
3. User data is retrieved from database
4. `AuthMeResponse` is returned

## Security Considerations

### Password Security
- Passwords must be hashed using bcrypt
- Minimum work factor of 12
- No plain text passwords in database

### Token Security
- JWTs must use strong signing algorithm (HS256/RS256)
- Short expiration times (15-30 minutes recommended)
- Secure storage on client-side

### Data Privacy
- Only minimal user information stored
- No sensitive information in JWT payload
- Email verification required for full access

## Migration Requirements

### Database Migration
```sql
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NULL,
    last_name VARCHAR(100) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    INDEX idx_email (email)
);
```

## Frontend Data Models

### User Session Model
```typescript
// frontend/src/types/auth.ts
export interface UserSession {
  user: {
    id: string;
    email: string;
    firstName?: string;
    lastName?: string;
  };
  token: string;
  isAuthenticated: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials extends LoginCredentials {
  firstName?: string;
  lastName?: string;
}
```

## API Contract Models

### Authentication Endpoints
```
POST /auth/register
Request: UserRegister
Response: AuthSuccessResponse

POST /auth/login
Request: UserLogin
Response: AuthSuccessResponse

GET /auth/me
Request: Authorization: Bearer <token>
Response: AuthMeResponse

POST /auth/logout
Request: Authorization: Bearer <token>
Response: AuthSuccessResponse
```

## Testing Data Models

### Test User Data
```python
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "TestPassword123!"
TEST_USER_FIRST_NAME = "Test"
TEST_USER_LAST_NAME = "User"
```

### Mock Token Data
```python
MOCK_JWT_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0X3VzZXJfaWQiLCJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJleHAiOjE3MzU2NzI4MDB9.example_signature"
```