# Todo App Frontend

This is the frontend for the Todo application built with Next.js 14+ using the App Router.

## Features

- **Authentication**: JWT-based authentication with login and signup
- **Protected Routes**: Routes that require authentication with automatic redirects
- **Public Routes**: Routes accessible without authentication
- **API Integration**: Centralized API client with automatic JWT token handling
- **Error Handling**: Consistent error handling for different HTTP status codes

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Install dependencies:
```bash
npm install
```

2. Set up environment variables:
```bash
# Copy the example environment file
cp .env.example .env.local
```

3. Update `.env.local` with your configuration:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-for-validation
```

### Running the Development Server

```bash
npm run dev
```

The application will be available at [http://localhost:3000](http://localhost:3000).

## Architecture

### Routing

The application uses Next.js App Router with the following route groups:

- `(auth)` - Public authentication routes (login, signup)
- `(protected)` - Routes requiring authentication (dashboard, profile)

### Authentication Flow

1. User accesses a route
2. If the route is protected and user is not authenticated, they are redirected to login
3. If user is authenticated and tries to access auth pages, they are redirected to dashboard
4. JWT tokens are stored in localStorage and attached to API requests automatically

### API Client

The application includes a centralized API client that:

- Automatically attaches JWT tokens to authenticated requests
- Handles 401 errors by logging out the user
- Handles 403 errors by showing access denied
- Handles 5xx errors with generic failure states

## Environment Variables

- `NEXT_PUBLIC_API_BASE_URL` - Base URL for the backend API
- `NEXT_PUBLIC_JWT_SECRET` - Secret for JWT token validation

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── (auth)/          # Public auth routes (login, signup)
│   │   ├── (protected)/     # Protected routes requiring auth
│   │   ├── layout.tsx       # Root layout
│   │   └── providers.tsx    # App providers (auth, theme, etc.)
│   ├── components/          # React components
│   │   ├── auth/            # Authentication-related components
│   │   ├── routing/         # Route protection components
│   │   └── error/           # Error display components
│   ├── contexts/            # React contexts (auth)
│   ├── hooks/               # Custom React hooks
│   ├── lib/                 # Library code
│   │   ├── api/             # API client and utilities
│   │   └── auth/            # Authentication utilities
│   └── utils/               # Utility functions
```

## Key Components

- `AuthProvider` - Manages authentication state
- `ProtectedRoute` - Component for protecting routes
- `PublicRoute` - Component for public routes with auth redirect
- `apiClient` - Centralized API client with JWT handling
- `useAuth` - Hook for accessing auth context
- `useApi` - Hook for making API calls with auth