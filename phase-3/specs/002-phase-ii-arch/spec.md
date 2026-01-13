# Phase II — Chunk 0: Foundation & Architecture (LOCK-IN)

## Status
DRAFT — Requires explicit approval before any implementation begins.

## Purpose
Establish immutable architectural decisions for Phase II of **The Evolution of Todo**.

This chunk exists to:
- Prevent rework
- Eliminate ambiguity
- Lock frontend/backend boundaries
- Define authentication trust and security model
- Provide a stable foundation for all future chunks

🚫 No code generation is allowed from this specification.
✅ All subsequent chunks MUST conform to this document.

---

## Scope
This specification covers:

- Monorepo structure and boundaries
- Frontend ↔ Backend responsibility split
- Authentication and authorization trust model
- JWT lifecycle and validation rules
- Environment variable ownership
- Failure states and security guarantees

---

## 1. Architecture Specification

### 1.1 Repository Structure (Monorepo)

The project SHALL use a **single monorepo** with clear separation between frontend and backend.

Top-level structure:

/frontend
/backend
/specs
/docs
/.env.example

#### Rules
- Frontend and backend MUST NOT share runtime code.
- Shared knowledge is allowed only through:
  - HTTP contracts
  - OpenAPI schemas
  - Written specifications
- No direct imports between frontend and backend are permitted.

### 1.2 Frontend Responsibilities (Untrusted)

The frontend is considered **fully untrusted**.

Frontend MAY:
- Render UI
- Collect user input
- Store tokens temporarily (memory or browser storage)
- Attach Authorization headers to requests

Frontend MUST NOT:
- Validate JWTs
- Make authorization decisions
- Trust local user state as authoritative
- Assume token validity without backend confirmation

Frontend decisions are considered **advisory only**.

### 1.3 Backend Responsibilities (Authoritative)

The backend is the **single source of truth**.

Backend MUST:
- Authenticate users
- Issue JWTs
- Validate all incoming tokens
- Enforce authorization rules
- Reject invalid, expired, or missing credentials

No request is trusted unless explicitly validated by the backend.

### 1.4 Environment Variables

Environment variables are split by responsibility.

#### Backend-Owned Secrets
- JWT secret / signing key
- Database credentials
- Token expiry configuration

These MUST:
- Never be exposed to the frontend
- Never be committed to source control

#### Frontend Configuration
- API base URL
- Public runtime flags

Frontend MUST NOT:
- Contain secrets
- Contain signing keys
- Derive security logic from env values

### 1.5 Folder Conventions (Backend)

Backend structure MUST logically separate:

- API routes
- Authentication logic
- Domain logic
- Persistence layer

Auth-related logic MUST NOT be embedded directly inside route handlers without abstraction.

## 2. Authentication & Authorization Specification

### 2.1 Authentication Strategy

The system SHALL use **JWT-based authentication**.

- Tokens are issued only by the backend
- Tokens represent authenticated identity
- Tokens are cryptographically signed
- Tokens have a finite lifetime

### 2.2 JWT Lifecycle

#### Issuance
JWTs are issued:
- After successful login
- After successful signup (if auto-login is enabled)

Each token MUST contain:
- A unique user identifier
- Issued-at timestamp
- Expiration timestamp

#### Storage (Client-Side)
- Storage mechanism is a frontend decision
- Backend assumes tokens can be leaked
- Token theft is mitigated via expiration and validation

#### Transmission
JWTs MUST be sent using the HTTP Authorization header.

Format:
Authorization: Bearer <token>

No other transport mechanism is considered valid.

### 2.3 Token Validation (Backend)

For every protected request, the backend MUST:

1. Check Authorization header existence
2. Validate header format
3. Verify token signature
4. Verify token expiration
5. Resolve user identity from token
6. Enforce authorization rules

Failure at ANY step results in request rejection.

### 2.4 Authorization Model

Authentication ≠ Authorization.

Backend MUST:
- Authenticate identity via JWT
- Authorize access per resource

Rules:
- Users may only access their own resources
- Ownership is enforced server-side
- Frontend filtering is NOT considered security

### 2.5 Failure States

#### 401 Unauthorized
Returned when:
- No token is provided
- Token is invalid
- Token is expired
- Token cannot be verified

#### 403 Forbidden
Returned when:
- Token is valid
- User is authenticated
- User lacks permission for the requested action

Frontend MUST treat:
- 401 as "not authenticated"
- 403 as "authenticated but not allowed"

### 2.6 Security Guarantees

The system guarantees:
- No unauthenticated access to protected routes
- No cross-user data access
- No reliance on frontend trust
- Explicit failure on all auth violations

## 3. User Scenarios & Testing

### 3.1 Authentication Flow
- As an unauthenticated user, I can access the login page
- As an authenticated user, I can access protected routes with valid JWT
- As a user with expired token, I am redirected to login
- As a user with invalid token, I receive 401 error

### 3.2 Authorization Flow
- As a user, I can only access my own data
- As a user, I receive 403 when attempting to access another user's data
- As an authenticated user, I can perform authorized actions
- As an unauthorized user, I cannot perform restricted actions

## 4. Functional Requirements

### 4.1 Monorepo Structure
- The system MUST maintain separate frontend and backend directories
- The system MUST NOT allow direct imports between frontend and backend code
- The system MUST define clear API contracts between frontend and backend

### 4.2 Authentication Requirements
- The system MUST issue JWT tokens upon successful authentication
- The system MUST validate JWT tokens for all protected endpoints
- The system MUST reject requests with invalid or expired tokens

### 4.3 Authorization Requirements
- The system MUST enforce user ownership of resources
- The system MUST prevent cross-user data access
- The system MUST return appropriate error codes for unauthorized access

### 4.4 Security Requirements
- The system MUST validate tokens server-side
- The system MUST NOT trust client-side state
- The system MUST implement proper error handling for security failures

## 5. Success Criteria

### 5.1 Architecture Success
- All frontend and backend code is properly separated
- No direct imports exist between frontend and backend
- Clear API contracts are established and documented

### 5.2 Security Success
- 100% of protected routes require valid JWT authentication
- Users can only access their own data resources
- Invalid/missing authentication results in proper 401/403 responses
- Security vulnerabilities are minimized through server-side validation

### 5.3 Performance Success
- Authentication validation adds minimal latency to requests
- Token validation completes within acceptable timeframes
- System handles concurrent authentication requests efficiently

## 6. Key Entities

### 6.1 User
- Unique identifier for each authenticated user
- Associated with personal data and resources
- Subject to authorization rules and access controls

### 6.2 JWT Token
- Contains user identity and metadata
- Has limited lifetime with expiration
- Cryptographically signed for integrity

### 6.3 Resource
- User-owned data entities
- Subject to ownership and access controls
- Protected by authorization mechanisms

## 7. Assumptions

- The frontend and backend will communicate via HTTP/HTTPS
- Better Auth will be used for JWT management
- Neon Serverless PostgreSQL will be used for data persistence
- Next.js and FastAPI will be the chosen frameworks
- The system will follow RESTful API principles

## 8. Dependencies

- Better Auth for authentication
- Neon Serverless PostgreSQL for data storage
- Next.js for frontend framework
- FastAPI for backend framework

## 9. Constraints

- No shared runtime code between frontend and backend
- All authentication validation must occur server-side
- Frontend must not make authorization decisions
- JWT tokens must follow standard format and validation

## Lock-In Clause

Once approved:
- This document becomes IMMUTABLE
- All future specs and implementations MUST comply
- Changes require a new versioned specification

Approval is REQUIRED before proceeding to:
🧱 CHUNK 1 — Backend Core & Persistence