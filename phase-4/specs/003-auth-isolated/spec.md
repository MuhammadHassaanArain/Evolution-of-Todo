# Phase II — Chunk 1: Authentication (ISOLATED)

## Status
DRAFT — Requires approval before implementation.

## Purpose
Authentication affects every system boundary.
This chunk isolates authentication concerns to prevent leakage into domain logic.

This specification defines:
- User authentication flows
- Session handling
- JWT validation
- Identity introspection

🚫 No Todo, task, or domain logic is allowed.
🚫 No authorization beyond identity validation.
✅ This chunk must be completed before any protected features.

---

## Scope

This chunk includes:

Frontend:
- Better Auth configuration
- Signup flow
- Login flow
- Logout flow
- Session persistence behavior

Backend:
- JWT validation dependency
- Authenticated identity extraction
- `/auth/me` protected endpoint

---

# 1.1 Authentication Model

## 1.1.1 Trust Boundary

- Frontend is **untrusted**
- Backend is **authoritative**
- JWT is the only proof of authentication

Frontend state is advisory only.

---

## 1.1.2 Authentication Strategy

The system SHALL use **JWT-based authentication**.

- Tokens are issued by the backend
- Tokens represent authenticated identity
- Tokens are validated on every protected request

Authentication ≠ Authorization
This chunk handles **identity only**.

---

# 1.2 Frontend Specification (Better Auth)

## 1.2.1 Better Auth Integration

Frontend SHALL use **Better Auth** as the authentication client.

Responsibilities:
- Initiate signup
- Initiate login
- Manage session state
- Attach JWT to requests

Frontend MUST NOT:
- Decode or validate JWTs for security decisions
- Enforce access control
- Assume token validity

---

## 1.2.2 Signup Flow

Signup flow SHALL:
1. Collect user credentials
2. Submit credentials to backend auth endpoint
3. Receive JWT upon success
4. Establish authenticated session

Failure cases:
- Invalid input
- Duplicate account
- Backend rejection

Frontend handles errors only for UX.

---

## 1.2.3 Login Flow

Login flow SHALL:
1. Collect credentials
2. Submit credentials to backend
3. Receive JWT upon success
4. Persist authenticated session

Invalid credentials MUST result in authentication failure without token issuance.

---

## 1.2.4 Logout Flow

Logout SHALL:
- Clear frontend session state
- Remove stored token (if any)

Logout does NOT:
- Invalidate JWT server-side (stateless model)

---

## 1.2.5 Session Persistence

Session persistence is a frontend concern.

Rules:
- Backend assumes tokens may persist or be stolen
- Token expiration is the primary security mechanism
- Frontend storage choice does not affect backend logic

---

# 1.3 Backend Specification

## 1.3.1 JWT Validation Dependency

Backend SHALL define a reusable JWT validation mechanism.

Responsibilities:
- Extract Authorization header
- Validate Bearer token format
- Verify signature
- Verify expiration
- Extract user identity

This dependency MUST:
- Reject invalid or missing tokens
- Fail fast
- Never trust client-provided identity

---

## 1.3.2 Authentication Dependency Output

On success, the validation dependency SHALL provide:
- Authenticated user identity
- Minimal identity context (e.g. user ID)

On failure:
- Request is rejected
- No identity is attached

---

## 1.3.3 Protected Endpoint: `/auth/me`

### Purpose
Provide authenticated identity introspection.

### Behavior
- Endpoint is protected by JWT validation
- Returns current authenticated user's identity
- No domain data is included

### Failure States
- 401 if token is missing or invalid
- Never returns data for unauthenticated requests

---

# 1.4 Failure Handling

## 1.4.1 401 Unauthorized

Returned when:
- Authorization header is missing
- Token is malformed
- Token is expired
- Token signature is invalid

---

## 1.4.2 Error Consistency

Backend MUST:
- Use consistent error responses
- Avoid leaking internal auth details
- Treat all auth failures as non-recoverable without re-authentication

---

# 1.5 Isolation Rules

This chunk MUST NOT:
- Reference Todo entities
- Reference task ownership
- Perform authorization checks
- Include role-based access logic

Only identity validation is allowed.

---

# 1.6 User Scenarios & Testing

## 1.6.1 User Scenarios

### Scenario 1: New User Registration
- As a new user, I can create an account with valid credentials
- As a new user, I receive a JWT token upon successful registration
- As a new user, my session is established in the frontend

### Scenario 2: Existing User Login
- As an existing user, I can log in with my credentials
- As an existing user, I receive a JWT token upon successful login
- As an existing user, my session is established in the frontend

### Scenario 3: Identity Verification
- As an authenticated user, I can verify my identity via `/auth/me` endpoint
- As an authenticated user, I receive my user information when presenting valid JWT
- As an unauthenticated user, I receive 401 error when accessing `/auth/me`

### Scenario 4: Session Management
- As a user, I can log out and have my session cleared
- As a user with expired token, I receive 401 error on protected endpoints
- As a user with invalid token, I receive 401 error on protected endpoints

---

# 1.7 Functional Requirements

## 1.7.1 Authentication Requirements
- The system MUST provide user registration endpoint that creates new user accounts
- The system MUST provide user login endpoint that validates credentials and issues JWT
- The system MUST provide user logout functionality that clears frontend session state
- The system MUST validate JWT tokens for all protected endpoints
- The system MUST reject requests with invalid, expired, or missing JWT tokens

## 1.7.2 Identity Requirements
- The system MUST provide `/auth/me` endpoint that returns authenticated user identity
- The system MUST extract user identity from valid JWT tokens
- The system MUST NOT return domain-specific data from identity endpoints
- The system MUST provide consistent identity information format

## 1.7.3 Security Requirements
- The system MUST validate JWT signature using appropriate algorithm
- The system MUST verify JWT expiration before accepting token
- The system MUST reject malformed JWT tokens
- The system MUST use consistent error responses for authentication failures

---

# 1.8 Success Criteria

## 1.8.1 Authentication Success
- 100% of valid registration requests result in account creation and JWT issuance
- 100% of valid login requests result in JWT token issuance
- 100% of invalid authentication requests result in 401 Unauthorized response
- Registration and login processes complete within acceptable timeframes

## 1.8.2 Identity Verification Success
- 100% of valid JWT requests to `/auth/me` return authenticated user identity
- 100% of invalid JWT requests to `/auth/me` return 401 Unauthorized response
- Identity information is returned in consistent, predictable format
- Identity verification completes quickly without performance degradation

## 1.8.3 Security Success
- 100% of malformed JWT tokens are rejected with 401 response
- 100% of expired JWT tokens are rejected with 401 response
- 100% of missing JWT tokens result in 401 response
- No security vulnerabilities exist in authentication flow

## 1.8.4 Usability Success
- Users can complete registration process without confusion
- Users can complete login process without confusion
- Error messages are clear and actionable for users
- Session management works consistently across different browsers/devices

---

# 1.9 Key Entities

## 1.9.1 User Identity
- Unique identifier for authenticated users
- Minimal information required for identity validation
- Subject to JWT token encoding requirements

## 1.9.2 JWT Token
- Contains user identity and metadata
- Has limited lifetime with expiration
- Cryptographically signed for integrity

---

# 1.10 Assumptions

- The frontend and backend will communicate via HTTP/HTTPS
- Better Auth will be used as the authentication framework
- JWT tokens will follow standard format and validation rules
- The system will operate in a stateless manner regarding authentication
- Token expiration will be the primary security mechanism for session management

---

# 1.11 Dependencies

- Better Auth framework for authentication management
- JWT libraries for token creation and validation
- Secure storage mechanism for secret keys
- HTTPS for secure token transmission

---

# 1.12 Constraints

- No domain logic implementation in this chunk
- No authorization checks beyond identity validation
- Stateless authentication model (no server-side session storage)
- Frontend cannot make security decisions based on token content
- All authentication validation must occur server-side

---

# Success Criteria

This chunk is considered complete when:

- A user can successfully sign up
- A user can successfully log in
- A JWT is issued by the backend
- Protected endpoints reject invalid or missing tokens
- `/auth/me` returns authenticated identity only when valid

---

## Lock-In Clause

Once approved:
- This specification is immutable
- Implementation MUST strictly follow this document
- All future chunks depend on this auth contract

Approval is REQUIRED before generating `auth.implement.md`.