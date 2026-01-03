# Quickstart: Frontend Routing & Data Access

## Setup

1. **Install Dependencies**
   ```bash
   cd frontend
   npm install next react react-dom typescript @types/react @types/node @types/react-dom
   npm install jose axios
   ```

2. **Environment Configuration**
   Set up required environment variables in `.env.local`:
   ```bash
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   NEXT_PUBLIC_JWT_SECRET=your-jwt-secret-for-validation
   ```

## Route Structure

### Public Routes (No Authentication Required)
- `/login` - User authentication page
- `/signup` - User registration page
- `/forgot-password` - Password recovery

### Protected Routes (Authentication Required)
- `/dashboard` - Main application dashboard
- `/profile` - User profile management
- `/todos` - Todo management interface

## Authentication Flow

### Protecting a Route
To protect a route, ensure it's located under the `(protected)` route group:
```
src/app/(protected)/dashboard/page.tsx
```

### Public Route Access
Public routes (like login/signup) should be in the `(auth)` route group:
```
src/app/(auth)/login/page.tsx
```

## API Client Usage

### Making Authenticated Requests
```typescript
import { useApi } from '../hooks/useApi';

const { data, error, loading } = useApi('/todos', {
  method: 'GET',
  requiresAuth: true
});
```

### Making Public Requests
```typescript
import { useApi } from '../hooks/useApi';

const { data, error, loading } = useApi('/public/health', {
  method: 'GET',
  requiresAuth: false
});
```

## Error Handling

The application handles API errors automatically:

- **401 Unauthorized**: User will be logged out and redirected to login
- **403 Forbidden**: Access denied page will be displayed
- **4xx Client Errors**: User-friendly error message displayed
- **5xx Server Errors**: Generic failure state with retry option

## Key Features

- **Centralized Authentication**: Auth state managed in a single provider
- **Route Protection**: Automatic redirect for unauthorized access
- **API Client**: Centralized request handling with auth header injection
- **Error Handling**: Consistent error responses across the application
- **Type Safety**: Full TypeScript support for API responses
- **Loading States**: Built-in loading and error states for API requests

## Testing the Implementation

1. Start the development server:
   ```bash
   npm run dev
   ```

2. Navigate to a protected route without authentication - you should be redirected to login

3. Authenticate and verify access to protected routes

4. Make API calls and verify JWT tokens are automatically attached

5. Test error scenarios by simulating 401/403 responses