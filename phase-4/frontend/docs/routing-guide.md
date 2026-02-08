# Frontend Routing Guide

This document explains the routing architecture and patterns used in the Todo application frontend.

## Overview

The application uses Next.js App Router with a clear separation between public and protected routes. Authentication state is managed centrally, and routing decisions are made based on this state.

## Route Structure

### Route Groups

The application uses Next.js route groups to organize different types of routes:

- `(auth)` - Contains public authentication routes (login, signup)
- `(protected)` - Contains routes that require authentication (dashboard, profile)

### Public Routes

Public routes are accessible without authentication:

- `/login` - User authentication page
- `/signup` - User registration page
- `/forgot-password` - Password recovery

### Protected Routes

Protected routes require an authenticated user:

- `/dashboard` - Main application dashboard
- `/profile` - User profile management
- `/todos` - Todo management interface

## Authentication Flow

### Unauthenticated User Accessing Protected Routes

1. User attempts to navigate to a protected route (e.g., `/dashboard`)
2. The `ProtectedLayout` component checks authentication status
3. If not authenticated, user is redirected to `/login` with the original path as a redirect parameter
4. After successful login, user is redirected back to the originally requested route

### Authenticated User Accessing Auth Pages

1. Authenticated user attempts to navigate to an auth page (e.g., `/login`)
2. The `PublicRoute` component or middleware detects the authenticated state
3. User is redirected to `/dashboard` (or another appropriate route)

## Implementation Details

### Route Protection

Route protection is implemented at multiple levels:

1. **Layout Level**: `ProtectedLayout` component checks authentication before rendering content
2. **Component Level**: `ProtectedRoute` and `PublicRoute` components provide additional protection
3. **Middleware Level**: Next.js middleware handles server-side redirects

### API Authentication

All API requests that require authentication automatically include the JWT token in the `Authorization` header. The API client handles:

- Attaching tokens to requests
- Handling 401 responses by logging out the user
- Handling 403 responses by showing access denied
- Handling 5xx responses with generic error states

## Components

### AuthProvider

The `AuthProvider` component manages authentication state across the application:

```tsx
<AuthProvider>
  {children}
</AuthProvider>
```

### useAuth Hook

The `useAuth` hook provides access to authentication state:

```tsx
const { isAuthenticated, user, login, logout, register } = useAuth();
```

### ProtectedRoute Component

The `ProtectedRoute` component ensures only authenticated users can access content:

```tsx
<ProtectedRoute>
  <div>Protected content</div>
</ProtectedRoute>
```

### PublicRoute Component

The `PublicRoute` component ensures only unauthenticated users can access auth pages:

```tsx
<PublicRoute>
  <LoginForm />
</PublicRoute>
```

## Error Handling

The application handles various authentication-related errors:

- **401 Unauthorized**: User is logged out and redirected to login
- **403 Forbidden**: Access denied page is displayed
- **4xx Client Errors**: User-friendly error messages are displayed
- **5xx Server Errors**: Generic failure states with retry options

## Best Practices

1. **Centralized Authentication**: Auth state is managed in a single provider
2. **Route Protection**: Automatic redirect for unauthorized access
3. **API Client**: Centralized request handling with auth header injection
4. **Error Handling**: Consistent error responses across the application
5. **Type Safety**: Full TypeScript support for API responses
6. **Loading States**: Built-in loading and error states for API requests