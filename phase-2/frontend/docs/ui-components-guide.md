# UI Components Guide

This document provides an overview of the UI components available in the application and how to use them.

## Table of Contents
1. [Button Component](#button-component)
2. [Input Component](#input-component)
3. [Textarea Component](#textarea-component)
4. [Select Component](#select-component)
5. [Task Components](#task-components)
6. [Layout Components](#layout-components)

## Button Component

The Button component provides various styles and sizes for interactive elements.

### Usage
```tsx
import { Button } from '../ui/button'

<Button variant="primary">Primary Button</Button>
<Button variant="secondary">Secondary Button</Button>
<Button variant="outline">Outline Button</Button>
<Button variant="destructive">Destructive Button</Button>
<Button variant="ghost">Ghost Button</Button>
<Button variant="link">Link Button</Button>
```

### Props
- `variant`: 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'destructive'
- `size`: 'sm' | 'md' | 'lg'
- `isLoading`: boolean - Shows loading spinner
- `leftIcon`, `rightIcon`: React.ReactNode - Icons to display
- `fullWidth`: boolean - Makes button full width
- Standard HTML button attributes

## Input Component

The Input component provides an accessible input field with labels and error handling.

### Usage
```tsx
import { Input } from '../ui/input'

<Input
  label="Username"
  placeholder="Enter your username"
  error={error}
  required
/>
```

### Props
- `label`: string - Label for the input
- `error`: string - Error message to display
- `helperText`: string - Helper text to display
- `required`: boolean - Whether the field is required
- `leftIcon`, `rightIcon`: React.ReactNode - Icons to display
- `variant`: 'default' | 'filled' | 'outline'
- `fullWidth`: boolean - Makes input full width
- Standard HTML input attributes

## Textarea Component

The Textarea component provides an accessible textarea with labels and error handling.

### Usage
```tsx
import { Textarea } from '../ui/input'

<Textarea
  label="Description"
  placeholder="Enter description"
  error={error}
  rows={4}
/>
```

### Props
- `label`: string - Label for the textarea
- `error`: string - Error message to display
- `helperText`: string - Helper text to display
- `required`: boolean - Whether the field is required
- `fullWidth`: boolean - Makes textarea full width
- Standard HTML textarea attributes

## Select Component

The Select component provides an accessible dropdown selection.

### Usage
```tsx
import { Select, SelectItem } from '../ui/select'

<Select label="Priority" value={value} onValueChange={handleChange}>
  <SelectItem value="low">Low Priority</SelectItem>
  <SelectItem value="medium">Medium Priority</SelectItem>
  <SelectItem value="high">High Priority</SelectItem>
</Select>
```

### Props
- `label`: string - Label for the select
- `error`: string - Error message to display
- `helperText`: string - Helper text to display
- `required`: boolean - Whether the field is required
- `disabled`: boolean - Whether the select is disabled
- Standard HTML select attributes

## Task Components

### TaskItem Component

Displays a single task with status indicators, priority levels, and due dates.

#### Props
- `id`: string | number - Task identifier
- `title`: string - Task title
- `description`: string - Task description (optional)
- `completed`: boolean - Whether the task is completed
- `createdAt`, `updatedAt`: string - Timestamps
- `priority`: 'low' | 'medium' | 'high' - Task priority
- `dueDate`: string - Due date (optional)
- `onToggle`, `onEdit`, `onDelete`: Functions for actions

### TaskList Component

Displays a list of tasks with filtering, sorting, and search capabilities.

#### Props
- `tasks`: Task[] - Array of tasks to display
- `onToggleTask`, `onEditTask`, `onDeleteTask`: Functions for task actions
- `title`: string - Title for the list (default: 'Tasks')
- `showFilters`, `showSearch`: boolean - Whether to show filters/search

### TaskForm Component

Form for creating and editing tasks with validation.

#### Props
- `initialValues`: TaskFormValues - Initial form values
- `onSubmit`: Function called when form is submitted
- `onCancel`: Function called when form is cancelled
- `submitText`: string - Text for submit button
- `isSubmitting`: boolean - Whether form is submitting

### EmptyState Component

Displays when there are no tasks to show.

#### Props
- `title`: string - Title for the empty state
- `description`: string - Description text
- `actionText`: string - Text for action button
- `onAction`: Function - Action to perform
- `icon`: ReactNode - Custom icon (optional)

### ConfirmationDialog Component

Modal dialog for confirming destructive actions like deletion.

#### Props
- `isOpen`: boolean - Whether dialog is open
- `title`: string - Dialog title
- `message`: string - Dialog message
- `confirmText`, `cancelText`: string - Button text
- `onConfirm`, `onCancel`: Functions for actions

## Layout Components

### Header Component

Responsive header with navigation elements.

### Footer Component

Responsive footer with information and links.

### Navigation Component

Responsive navigation with menu items.

## Hooks

### useUndo Hook

Provides undo/redo functionality for state management.

#### Usage
```tsx
import { useUndo } from '../hooks/use-undo'

const { state, setState, undo, redo, canUndo, canRedo, reset } = useUndo(initialValue)
```

## Accessibility Features

All components include:
- Proper ARIA attributes
- Keyboard navigation support
- Focus management
- Screen reader compatibility
- Semantic HTML structure
- Color contrast compliance

## Styling

Components use Tailwind CSS utility classes with:
- Consistent spacing system
- Themeable color palette
- Responsive design patterns
- Visual feedback states
- Smooth transitions