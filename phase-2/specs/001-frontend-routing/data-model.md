# Data Model: Frontend Routing & Data Access

## Entity: Route

**Fields**:
- `path` (string) - The URL path for the route
- `isProtected` (boolean) - Whether the route requires authentication
- `redirectPath` (string, optional) - Where to redirect if not authenticated (for protected routes)
- `component` (ReactComponent) - The UI component to render for this route

**Relationships**:
- Belongs to an `AuthProvider` that manages authentication state for route access

**Validation Rules**:
- `path` must be a valid URL path
- If `isProtected` is true, `redirectPath` should be defined

## Entity: AuthSession

**Fields**:
- `token` (string) - JWT token for authentication
- `expiresAt` (datetime) - When the token expires
- `userId` (string) - ID of the authenticated user
- `isAuthenticated` (boolean) - Whether the session is valid

**Relationships**:
- Associated with multiple `Route` entities that require authentication
- Associated with `ApiClient` to provide authentication headers

**Validation Rules**:
- `token` must be a valid JWT format
- `expiresAt` must be in the future for valid sessions
- `userId` must be present for authenticated sessions

## Entity: ApiRequest

**Fields**:
- `url` (string) - Target API endpoint
- `method` (string) - HTTP method (GET, POST, PUT, DELETE)
- `headers` (object) - Request headers including Authorization
- `body` (any, optional) - Request body for POST/PUT requests

**Relationships**:
- Uses `AuthSession` to add authorization headers
- Produces `ApiResponse` entities

**Validation Rules**:
- `url` must be a valid API endpoint
- `method` must be a valid HTTP method
- If authenticated, Authorization header must be included

## Entity: ApiResponse

**Fields**:
- `status` (number) - HTTP status code
- `data` (any) - Response data from the API
- `error` (string, optional) - Error message if request failed
- `timestamp` (datetime) - When the response was received

**Relationships**:
- Result of an `ApiRequest` entity
- May trigger `AuthSession` updates (e.g., on 401 responses)

**Validation Rules**:
- `status` must be a valid HTTP status code
- If status indicates error, `error` field should be populated

## Entity: ApiClient

**Fields**:
- `baseUrl` (string) - Base URL for API requests
- `defaultHeaders` (object) - Default headers to include in all requests
- `interceptors` (array) - Functions to process requests/responses

**Relationships**:
- Uses `AuthSession` to add authentication headers
- Processes multiple `ApiRequest` entities
- Produces multiple `ApiResponse` entities

**Validation Rules**:
- `baseUrl` must be a valid URL
- `interceptors` must be valid functions