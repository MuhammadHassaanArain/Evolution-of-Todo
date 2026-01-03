# Research: Frontend Routing & Data Access

## Decision: Next.js App Router Implementation
**Rationale**: Following the specification requirement to use Next.js App Router. This provides built-in support for file-based routing, layout nesting, and server-side rendering capabilities that align well with the authentication boundary requirements.

**Alternatives considered**:
- Page Router (rejected - App Router is more modern and provides better layout capabilities)
- Client-side routing libraries (rejected - Next.js provides better performance and SEO)
- Other frameworks (rejected - specification requires Next.js)

## Decision: Authentication State Management Approach
**Rationale**: Using React Context API with a centralized AuthProvider to manage authentication state. This allows components throughout the app to access authentication status without prop drilling while maintaining a single source of truth.

**Alternatives considered**:
- Redux/Zustand (rejected - Context API is sufficient for auth state)
- URL-based auth (rejected - less secure and harder to maintain)
- Component-scoped auth checks (rejected - violates specification requirement for centralized checks)

## Decision: Protected vs Public Route Organization
**Rationale**: Using Next.js route groups with `(auth)` and `(protected)` directories to logically separate public and protected routes. This makes the routing structure clear and enforces the authentication boundary at the file system level.

**Alternatives considered**:
- Individual route protection (rejected - harder to maintain and doesn't scale)
- Server-side auth checking only (rejected - client-side UX improvements needed)
- Mixed route organization (rejected - specification requires clear boundaries)

## Decision: API Client Architecture
**Rationale**: Implementing a centralized API client that automatically attaches JWT tokens and handles common error responses. This ensures consistent API communication across the application and meets the specification requirement for centralized API handling.

**Alternatives considered**:
- Direct fetch calls (rejected - violates specification requirement for centralized client)
- Multiple API clients (rejected - harder to maintain consistency)
- Third-party HTTP libraries (rejected - native fetch with custom wrapper provides better control)

## Decision: Error Handling Strategy
**Rationale**: Centralized error handling in the API client that maps HTTP status codes to appropriate responses per the specification (401 → logout, 403 → access denied, etc.). This ensures consistent error behavior across all API interactions.

**Alternatives considered**:
-分散错误处理 (rejected - leads to inconsistent behavior)
- Generic error handler only (rejected - specification requires specific handling per status code)
- Server-side error handling only (rejected - client-side UX improvements needed)

## Decision: Session Storage Mechanism
**Rationale**: Using localStorage for JWT token storage with appropriate security considerations. This allows for persistent sessions across browser sessions while keeping the token accessible to the frontend for API requests.

**Alternatives considered**:
- Cookies (rejected - specification suggests client-side storage)
- SessionStorage (rejected - doesn't persist across browser restarts)
- Memory only (rejected - requires re-authentication on page refresh)