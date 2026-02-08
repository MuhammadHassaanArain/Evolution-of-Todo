# Quickstart Guide: UI Redesign for Todo Application

## Overview
This guide provides the essential information to begin implementing the UI redesign for the todo application. It covers the setup, key technologies, and initial steps required to start development.

## Prerequisites

### Environment Setup
- Node.js 18+ (or latest LTS)
- npm or yarn package manager
- Git version control
- Text editor or IDE with TypeScript/JavaScript support

### Project Dependencies
The following dependencies will be used for the UI redesign:

```bash
# Core dependencies
npm install next react react-dom typescript @types/react @types/node
npm install tailwindcss postcss autoprefixer

# UI and animation libraries
npm install framer-motion
npm install @heroicons/react # For UI icons

# Form handling
npm install react-hook-form

# State management (if needed)
npm install zustand # or jotai for lightweight state management

# Accessibility
npm install @headlessui/react # For accessible UI components
```

## Development Setup

### 1. Initialize Next.js Project
```bash
# Navigate to the frontend directory
cd frontend

# Initialize a new Next.js project
npx create-next-app@latest . --typescript --eslint --tailwind --src-dir --app --no-import-alias

# Or if starting fresh in the frontend directory
mkdir frontend && cd frontend
npx create-next-app@latest . --typescript --eslint --tailwind --src-dir --app --no-import-alias
```

### 2. Configure Tailwind CSS
```bash
# Initialize Tailwind configuration
npx tailwindcss init -p
```

Update `tailwind.config.js`:
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class', // Enable dark mode with class strategy
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        secondary: {
          500: '#8b5cf6',
          600: '#7c3aed',
        },
        success: {
          500: '#22c55e',
        },
        warning: {
          500: '#f59e0b',
        },
        error: {
          500: '#ef4444',
        },
      },
      spacing: {
        '1.25': '0.3125rem', // 5px for 8px grid system
        '2.25': '0.5625rem', // 9px
        '3.5': '0.875rem',   // 14px
        '18': '4.5rem',      // 72px
      },
    },
  },
  plugins: [],
}
```

### 3. Configure TypeScript
Update `tsconfig.json` with appropriate settings for Next.js 16+.

## Key Implementation Steps

### 1. Set Up Project Structure
Create the following directory structure in the `frontend/src` directory:

```
components/
├── ui/                    # Reusable UI components
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   ├── Modal.tsx
│   └── ...
├── auth/                  # Authentication components
│   ├── SignInForm.tsx
│   ├── SignUpForm.tsx
│   └── ...
├── todos/                 # Todo-specific components
│   ├── TodoCard.tsx
│   ├── TodoList.tsx
│   ├── TodoModal.tsx
│   └── ...
├── layout/                # Layout components
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   ├── Navigation.tsx
│   └── ...
└── common/                # Shared/common components
    ├── EmptyState.tsx
    ├── LoadingSpinner.tsx
    └── ...
```

### 2. Implement Responsive Design
Use Tailwind's responsive prefixes to implement the required breakpoints:

```jsx
// Example of responsive component
<div className="
  w-full
  md:w-96
  lg:w-128
  p-4
  rounded-lg
  shadow-md
">
  {/* Content */}
</div>
```

Breakpoints to implement:
- Mobile: `<640px` (use base styles or `sm:` prefix)
- Tablet: `640px-1024px` (use `md:` prefix)
- Desktop: `>1024px` (use `lg:` or `xl:` prefix)

### 3. Implement Dark Mode Support
Add dark mode classes to all components:

```jsx
// Example of dark mode support
<button className="
  bg-primary-500
  text-white
  hover:bg-primary-600
  dark:bg-primary-600
  dark:hover:bg-primary-700
  px-4
  py-2
  rounded
">
  Button
</button>
```

### 4. Create Authentication Pages
Implement sign-in and sign-up pages with:
- Centered card layout
- Form validation
- Loading states
- Error handling
- Password visibility toggle
- Smooth transitions

### 5. Implement Todo Dashboard
Create the main dashboard with:
- Header with user profile
- Responsive sidebar for filters
- Todo list with card-based layout
- Add todo button
- Search and filter functionality

### 6. Add Animations and Transitions
Use Framer Motion for smooth animations:

```tsx
import { motion } from 'framer-motion';

// Example animation
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
  {/* Content */}
</motion.div>
```

## API Integration

### Existing Backend Endpoints
The UI will connect to the existing backend API without changes. Key endpoints:

- `GET /api/todos` - Retrieve user's todos
- `POST /api/todos` - Create new todo
- `PUT /api/todos/{id}` - Update todo
- `DELETE /api/todos/{id}` - Delete todo
- `POST /api/auth/signin` - User sign in
- `POST /api/auth/signup` - User sign up

### API Service Layer
Create a service layer to handle API communication:

```typescript
// frontend/src/services/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const apiClient = {
  get: async (endpoint: string, token?: string) => {
    const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
    const response = await fetch(`${API_BASE_URL}${endpoint}`, { headers });
    return response.json();
  },

  post: async (endpoint: string, data: any, token?: string) => {
    // Implementation
  },

  put: async (endpoint: string, data: any, token?: string) => {
    // Implementation
  },

  delete: async (endpoint: string, token?: string) => {
    // Implementation
  }
};
```

## Accessibility Implementation

### Semantic HTML
Use proper semantic elements:
- `<main>` for main content
- `<nav>` for navigation
- `<aside>` for sidebar content
- `<section>` for content sections
- `<article>` for todo items

### ARIA Attributes
Add appropriate ARIA attributes:
- `aria-label` for icon buttons
- `role="alert"` for error messages
- `aria-live="polite"` for dynamic content updates
- `aria-expanded` for collapsible elements

### Keyboard Navigation
Ensure all interactive elements are keyboard accessible:
- Proper tab order
- Focus indicators
- Keyboard event handlers (Enter, Space, Escape)

## Testing Strategy

### Component Testing
Use Jest and React Testing Library to test components:

```bash
npm install -D jest @testing-library/react @testing-library/jest-dom @testing-library/user-event
```

### Accessibility Testing
Include accessibility tests in the test suite:

```bash
npm install -D axe-core jest-axe
```

## Build and Deployment

### Development Build
```bash
npm run dev
```

### Production Build
```bash
npm run build
```

### Preview Production Build
```bash
npm run start
```

## Next Steps

1. Begin with authentication pages (sign-in/sign-up)
2. Implement the main dashboard layout
3. Add todo list functionality
4. Create todo creation/editing components
5. Add animations and polish
6. Implement responsive design
7. Add accessibility features
8. Test across browsers and devices