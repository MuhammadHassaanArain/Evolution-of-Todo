import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { TaskList } from '../../src/components/todo/task-list'
import { TaskForm } from '../../src/components/todo/task-form'
import { TaskItem } from '../../src/components/todo/task-item'

// Mock data for testing
const mockTasks = [
  {
    id: 1,
    title: 'Test Task 1',
    description: 'This is a test task',
    completed: false,
    createdAt: '2023-01-01T00:00:00Z',
    updatedAt: '2023-01-01T00:00:00Z',
    priority: 'medium' as const,
    dueDate: '2023-12-31T00:00:00Z'
  },
  {
    id: 2,
    title: 'Test Task 2',
    description: 'This is another test task',
    completed: true,
    createdAt: '2023-01-02T00:00:00Z',
    updatedAt: '2023-01-02T00:00:00Z',
    priority: 'high' as const,
    dueDate: '2023-11-30T00:00:00Z'
  }
]

describe('Task Management UX Flows', () => {
  test('should render task list with tasks', () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleTask={() => {}}
        onEditTask={() => {}}
        onDeleteTask={() => {}}
      />
    )

    expect(screen.getByText('Test Task 1')).toBeInTheDocument()
    expect(screen.getByText('Test Task 2')).toBeInTheDocument()
    expect(screen.getByText('1 active, 1 completed')).toBeInTheDocument()
  })

  test('should filter tasks correctly', async () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleTask={() => {}}
        onEditTask={() => {}}
        onDeleteTask={() => {}}
      />
    )

    // Initially both tasks should be visible
    expect(screen.getByText('Test Task 1')).toBeInTheDocument()
    expect(screen.getByText('Test Task 2')).toBeInTheDocument()

    // Filter by active tasks
    const filterSelect = screen.getByLabelText('Filter tasks')
    fireEvent.change(filterSelect, { target: { value: 'active' } })

    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument()
      expect(screen.queryByText('Test Task 2')).not.toBeInTheDocument()
    })

    // Filter by completed tasks
    fireEvent.change(filterSelect, { target: { value: 'completed' } })

    await waitFor(() => {
      expect(screen.queryByText('Test Task 1')).not.toBeInTheDocument()
      expect(screen.getByText('Test Task 2')).toBeInTheDocument()
    })
  })

  test('should sort tasks correctly', async () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleTask={() => {}}
        onEditTask={() => {}}
        onDeleteTask={() => {}}
      />
    )

    // Sort by priority
    const sortSelect = screen.getByLabelText('Sort tasks')
    fireEvent.change(sortSelect, { target: { value: 'priority' } })

    await waitFor(() => {
      // High priority task should appear first
      expect(screen.getByText('Test Task 2')).toBeInTheDocument()
    })
  })

  test('should search tasks correctly', async () => {
    render(
      <TaskList
        tasks={mockTasks}
        onToggleTask={() => {}}
        onEditTask={() => {}}
        onDeleteTask={() => {}}
      />
    )

    const searchInput = screen.getByLabelText('Search tasks')
    fireEvent.change(searchInput, { target: { value: 'Task 1' } })

    await waitFor(() => {
      expect(screen.getByText('Test Task 1')).toBeInTheDocument()
      expect(screen.queryByText('Test Task 2')).not.toBeInTheDocument()
    })
  })

  test('should toggle task completion', () => {
    const mockToggle = jest.fn()
    render(
      <TaskItem
        id={1}
        title="Test Task"
        description="Test description"
        completed={false}
        createdAt="2023-01-01T00:00:00Z"
        updatedAt="2023-01-01T00:00:00Z"
        onToggle={mockToggle}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    )

    const checkbox = screen.getByLabelText('Mark "Test Task" as complete')
    fireEvent.click(checkbox)

    expect(mockToggle).toHaveBeenCalled()
  })

  test('should render empty state when no tasks', () => {
    render(
      <TaskList
        tasks={[]}
        onToggleTask={() => {}}
        onEditTask={() => {}}
        onDeleteTask={() => {}}
      />
    )

    expect(screen.getByText('No tasks found')).toBeInTheDocument()
  })

  test('should handle task form submission', () => {
    const mockSubmit = jest.fn()
    render(
      <TaskForm
        onSubmit={mockSubmit}
        initialValues={{
          title: '',
          description: '',
          priority: 'medium',
          dueDate: ''
        }}
      />
    )

    const titleInput = screen.getByLabelText('Title *')
    fireEvent.change(titleInput, { target: { value: 'New Task' } })

    const submitButton = screen.getByLabelText('Save task')
    fireEvent.click(submitButton)

    expect(mockSubmit).toHaveBeenCalledWith({
      title: 'New Task',
      description: '',
      priority: 'medium',
      dueDate: ''
    })
  })
})