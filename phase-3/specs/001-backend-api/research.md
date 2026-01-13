# Research: Backend API (Business Logic)

## Decision: FastAPI Framework for Backend API
**Rationale**: Following the constitution requirement to use FastAPI for the backend API. FastAPI provides excellent support for JWT authentication, automatic OpenAPI documentation, and async capabilities which are well-suited for a todo management API.

**Alternatives considered**:
- Flask (rejected - FastAPI provides better automatic documentation and performance)
- Django (rejected - overkill for this API-focused application)
- Express.js (rejected - constitution specifies Python with FastAPI)

## Decision: JWT Authentication Implementation
**Rationale**: Following the specification requirement and constitution mandate to use JWT for authentication. JWT tokens will be validated on every request to ensure proper user ownership enforcement.

**Alternatives considered**:
- Session-based authentication (rejected - JWT is stateless and better for API scalability)
- OAuth2 (rejected - JWT with Better Auth is sufficient for this use case)
- API keys (rejected - JWT provides user context needed for ownership checks)

## Decision: Todo Ownership Enforcement Strategy
**Rationale**: Ownership will be enforced server-side on every request by checking the JWT token to identify the user and then verifying that any todo being accessed belongs to that user. This prevents cross-user data exposure.

**Alternatives considered**:
- Client-side ownership enforcement (rejected - security risk, client cannot be trusted)
- Database-level enforcement only (rejected - need application-level checks for complete security)
- Caching ownership information (rejected - adds complexity, direct validation preferred)

## Decision: Error Response Format
**Rationale**: Following REST API best practices with consistent error response format. All errors will return appropriate HTTP status codes with descriptive error messages in JSON format.

**Alternatives considered**:
- Different error formats (rejected - standard JSON format is expected by clients)
- Plain text errors (rejected - JSON is more structured and machine-readable)

## Decision: Request/Response Schema Validation
**Rationale**: Using Pydantic models for request/response validation to ensure data integrity and provide automatic documentation. This follows FastAPI's native capabilities.

**Alternatives considered**:
- Manual validation (rejected - Pydantic provides better validation and documentation)
- Different validation libraries (rejected - Pydantic is standard with FastAPI)
- No validation (rejected - security and data integrity requirements mandate validation)

## Decision: API Endpoint Structure
**Rationale**: Following RESTful principles with endpoints like `/todos` for collections and `/todos/{id}` for individual resources. This provides a clean, predictable API structure.

**Alternatives considered**:
- RPC-style endpoints (rejected - RESTful is more standard and discoverable)
- Different URL patterns (rejected - standard REST patterns are well-understood)