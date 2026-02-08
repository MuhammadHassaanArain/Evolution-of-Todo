# Data Model: UI Redesign for Todo Full-Stack Web Application

## Overview
This document outlines the data structures and entities relevant to the UI redesign, focusing on how data is represented in the frontend layer. The actual data persistence remains with the backend and database as defined in the existing system.

## UI-Specific Data Models

### 1. Todo Item (Frontend Representation)
Represents a todo item as displayed and managed in the UI

```typescript
interface TodoItem {
  id: string;                    // Unique identifier for the todo
  title: string;                 // Title of the todo (required)
  description?: string;          // Optional description of the todo
  completed: boolean;            // Completion status (true/false)
  priority: 'low' | 'medium' | 'high'; // Priority level (color-coded)
  dueDate?: string;              // Optional due date (ISO 8601 format)
  createdAt: string;             // Creation timestamp (ISO 8601 format)
  updatedAt: string;             // Last update timestamp (ISO 8601 format)
  userId: string;                // Owner of the todo (for display purposes)
}
```

**Validation rules from requirements**:
- title is required (non-empty string)
- priority must be one of 'low', 'medium', 'high'
- dueDate, if present, must be a valid ISO 8601 date string
- createdAt and updatedAt must be valid ISO 8601 date strings

**UI-specific behaviors**:
- Visual representation varies based on completion status (strikethrough, color)
- Priority affects badge color (low: gray, medium: yellow, high: red)
- Due date may show as relative time (e.g., "due tomorrow")

### 2. Filter Options
Configuration object for filtering and sorting todos

```typescript
interface FilterOptions {
  status?: 'all' | 'active' | 'completed';  // Filter by completion status
  priority?: 'all' | 'low' | 'medium' | 'high'; // Filter by priority
  sortBy?: 'createdAt' | 'updatedAt' | 'dueDate' | 'priority'; // Sort field
  sortOrder?: 'asc' | 'desc';              // Sort direction
  searchQuery?: string;                    // Text search query
}
```

**State transitions**:
- Changes trigger re-rendering of the todo list
- Applied in real-time as user interacts with filter controls

### 3. UI State Management
Frontend state for managing UI interactions

```typescript
interface TodoUIState {
  todos: TodoItem[];             // Current list of todos displayed
  loading: boolean;              // Loading state for data fetching
  creating: boolean;             // Loading state for todo creation
  editingId: string | null;     // ID of todo currently being edited
  error: string | null;         // Error message if any operation fails
  filters: FilterOptions;       // Current filter configuration
  searchTerm: string;           // Current search term
  showCreateModal: boolean;     // Whether to show create todo modal
  showDeleteConfirm: string | null; // ID of todo to confirm deletion
}
```

### 4. User Session (Frontend Representation)
Represents the authenticated user session for UI purposes

```typescript
interface UserSession {
  id: string;                   // User ID
  email: string;                // User email
  name?: string;                // Optional display name
  isAuthenticated: boolean;     // Authentication status
  isLoading: boolean;           // Authentication state loading
  error: string | null;         // Authentication error if any
}
```

### 5. Form State (Create/Edit Todo)
State management for the todo creation/editing form

```typescript
interface TodoFormState {
  title: string;                // Todo title (required)
  description: string;          // Todo description
  priority: 'low' | 'medium' | 'high'; // Priority level
  dueDate: string;              // Due date (ISO string format)
  errors: {
    title?: string;             // Title validation error
    description?: string;       // Description validation error
    dueDate?: string;          // Due date validation error
  };
  isValid: boolean;             // Form validity state
  submitting: boolean;         // Submission loading state
}
```

**Validation rules**:
- title must be non-empty
- dueDate, if present, must be valid date format
- Form is valid only when all required fields are filled correctly

### 6. Theme Configuration
Settings for dark/light mode

```typescript
interface ThemeConfig {
  mode: 'light' | 'dark' | 'system'; // Theme preference
  isDarkMode: boolean;          // Current active theme (derived from mode)
}
```

## UI Component Data Flows

### Todo List Component
- Receives: Array of TodoItem objects
- Emits: Events for todo completion, editing, deletion
- Internal state: Pagination, filtering, sorting

### Todo Card Component
- Receives: Single TodoItem object
- Emits: Events for completion toggle, edit, delete
- Internal state: Hover effects, animation states

### Filter Sidebar Component
- Receives: Current filter configuration
- Emits: Filter change events
- Internal state: Expanded/collapsed state on mobile

### Create/Edit Modal Component
- Receives: Initial todo data (for editing) or empty state (for creation)
- Emits: Save/cancel events with form data
- Internal state: Form validation, submission status

## State Transitions

### Todo Completion
1. User clicks checkbox
2. UI temporarily updates visual state
3. API call initiated
4. On success, state permanently updated
5. On failure, state reverted with error notification

### Todo Creation
1. User opens modal/form
2. Form state initialized
3. User fills form
4. Validation applied
5. On submit, loading state activated
6. API call made
7. On success, new todo added to list
8. On failure, error displayed

### Filter Application
1. User selects filter options
2. Filters state updated
3. Todo list re-queried/re-filtered
4. New list rendered

## Performance Considerations

### Client-Side Optimization
- Virtual scrolling for large todo lists
- Debounced search input
- Memoization of expensive computations
- Lazy loading of components when possible

### Data Fetching
- Caching of todo data
- Optimistic updates for better UX
- Error handling and retry mechanisms
- Loading states for all async operations