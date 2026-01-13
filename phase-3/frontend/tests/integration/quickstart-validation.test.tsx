import { render, screen } from '@testing-library/react'
import { TaskList } from '../../src/components/todo/task-list'
import { TaskItem } from '../../src/components/todo/task-item'
import { TaskForm } from '../../src/components/todo/task-form'

describe('Quickstart Validation Tests', () => {
  test('TaskList component should render correctly', () => {
    render(
      <TaskList
        tasks={[
          {
            id: 1,
            title: 'Test Task',
            completed: false,
            createdAt: '2023-01-01T00:00:00Z',
            updatedAt: '2023-01-01T00:00:00Z',
          }
        ]}
        onToggleTask={() => {}}
        onEditTask={() => {}}
        onDeleteTask={() => {}}
      />
    )

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('1 active, 0 completed')).toBeInTheDocument()
  })

  test('TaskItem component should render correctly', () => {
    render(
      <TaskItem
        id={1}
        title="Test Task"
        description="Test description"
        completed={false}
        createdAt="2023-01-01T00:00:00Z"
        updatedAt="2023-01-01T00:00:00Z"
        onToggle={() => {}}
        onEdit={() => {}}
        onDelete={() => {}}
      />
    )

    expect(screen.getByText('Test Task')).toBeInTheDocument()
    expect(screen.getByText('Test description')).toBeInTheDocument()
  })

  test('TaskForm component should render correctly', () => {
    render(
      <TaskForm
        onSubmit={() => {}}
        initialValues={{
          title: 'Test Task',
          description: 'Test description',
          priority: 'medium',
          dueDate: ''
        }}
      />
    )

    expect(screen.getByLabelText('Title *')).toBeInTheDocument()
    expect(screen.getByLabelText('Description')).toBeInTheDocument()
  })
})