import { render, screen, fireEvent } from '@testing-library/react'
import { TaskList } from '../../src/components/todo/task-list'
import { TaskItem } from '../../src/components/todo/task-item'
import { TaskForm } from '../../src/components/todo/task-form'
import { TaskFeedback } from '../../src/components/todo/task-feedback'
import { ConfirmationDialog } from '../../src/components/todo/confirmation-dialog'

describe('Integration Tests', () => {
  test('Task components should work together', () => {
    const mockTasks = [
      {
        id: 1,
        title: 'Test Task 1',
        completed: false,
        createdAt: '2023-01-01T00:00:00Z',
        updatedAt: '2023-01-01T00:00:00Z',
      },
      {
        id: 2,
        title: 'Test Task 2',
        completed: true,
        createdAt: '2023-01-01T00:00:00Z',
        updatedAt: '2023-01-01T00:00:00Z',
      }
    ]

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

  test('TaskForm and TaskList should integrate properly', () => {
    render(
      <div>
        <TaskForm
          onSubmit={() => {}}
          initialValues={{
            title: 'New Task',
            description: 'Task description',
            priority: 'medium',
            dueDate: ''
          }}
        />
        <TaskList
          tasks={[]}
          onToggleTask={() => {}}
          onEditTask={() => {}}
          onDeleteTask={() => {}}
        />
      </div>
    )

    expect(screen.getByLabelText('Title *')).toBeInTheDocument()
    expect(screen.getByText('No tasks found')).toBeInTheDocument()
  })

  test('TaskFeedback should display correctly', () => {
    render(
      <TaskFeedback
        message="Task created successfully"
        type="success"
        visible={true}
      />
    )

    expect(screen.getByText('Task created successfully')).toBeInTheDocument()
  })

  test('ConfirmationDialog should render when open', () => {
    render(
      <ConfirmationDialog
        isOpen={true}
        title="Confirm Deletion"
        message="Are you sure you want to delete this task?"
        confirmText="Delete"
        cancelText="Cancel"
        onConfirm={() => {}}
        onCancel={() => {}}
      />
    )

    expect(screen.getByText('Confirm Deletion')).toBeInTheDocument()
    expect(screen.getByText('Are you sure you want to delete this task?')).toBeInTheDocument()
  })
})