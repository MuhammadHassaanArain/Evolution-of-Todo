'use client'

import React, { useState } from 'react'
import { TaskItem } from './task-item'
import { EmptyState } from './empty-state'
import { cn } from '../../lib/utils'

export interface Task {
  id: string | number
  title: string
  description?: string
  completed: boolean
  created_at: string  // Updated to match backend format
  updated_at: string  // Updated to match backend format
  priority?: 'low' | 'medium' | 'high'
  due_date?: string  // Updated to match backend format
}

export interface TaskListProps {
  tasks: Task[]
  onToggleTask?: (id: string | number) => void
  onEditTask?: (id: string | number) => void
  onDeleteTask?: (id: string | number) => void
  className?: string
  title?: string
  emptyStateText?: string
  showFilters?: boolean
  showSearch?: boolean
}

export const TaskList: React.FC<TaskListProps> = ({
  tasks,
  onToggleTask,
  onEditTask,
  onDeleteTask,
  className,
  title = 'Tasks',
  emptyStateText = 'No tasks yet. Add your first task to get started.',
  showFilters = true,
  showSearch = true,
  ...props
}) => {
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all')
  const [searchTerm, setSearchTerm] = useState('')
  const [sortOption, setSortOption] = useState<'newest' | 'oldest' | 'priority'>('newest')

  // Filter tasks based on the selected filter and search term
  const filteredTasks = tasks.filter(task => {
    // Apply filter
    if (filter === 'active' && task.completed) return false
    if (filter === 'completed' && !task.completed) return false

    // Apply search
    if (
      searchTerm &&
      !task.title.toLowerCase().includes(searchTerm.toLowerCase()) &&
      !(task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()))
    ) {
      return false
    }

    return true
  })

  // Sort tasks based on selected option
  const sortedTasks = [...filteredTasks].sort((a, b) => {
    if (sortOption === 'newest') {
      return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()  // Updated field name
    } else if (sortOption === 'oldest') {
      return new Date(a.created_at).getTime() - new Date(b.created_at).getTime()  // Updated field name
    } else if (sortOption === 'priority') {
      const priorityOrder = { high: 3, medium: 2, low: 1 }
      return (priorityOrder[b.priority || 'medium'] || 2) - (priorityOrder[a.priority || 'medium'] || 2)
    }
    return 0
  })

  // Count completed and active tasks
  const completedCount = tasks.filter(task => task.completed).length
  const activeCount = tasks.length - completedCount

  return (
    <div className={cn('bg-white rounded-lg shadow', className)} {...props}>
      <div className="p-6 border-b border-gray-200">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <h2 className="text-xl font-bold text-gray-900">{title}</h2>

          {tasks.length > 0 && (
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-500">
                {activeCount} active, {completedCount} completed
              </div>

              {showFilters && (
                <div className="flex space-x-2">
                  <select
                    value={filter}
                    onChange={(e) => setFilter(e.target.value as 'all' | 'active' | 'completed')}
                    className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    aria-label="Filter tasks"
                  >
                    <option value="all">All Tasks</option>
                    <option value="active">Active</option>
                    <option value="completed">Completed</option>
                  </select>

                  <select
                    value={sortOption}
                    onChange={(e) => setSortOption(e.target.value as 'newest' | 'oldest' | 'priority')}
                    className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    aria-label="Sort tasks"
                  >
                    <option value="newest">Newest First</option>
                    <option value="oldest">Oldest First</option>
                    <option value="priority">Priority</option>
                  </select>
                </div>
              )}
            </div>
          )}
        </div>

        {showSearch && (
          <div className="mt-4">
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full sm:w-64 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              aria-label="Search tasks"
            />
          </div>
        )}
      </div>

      <div className="divide-y divide-gray-200">
        {sortedTasks.length > 0 ? (
          sortedTasks.map((task) => (
            <TaskItem
              key={task.id}
              id={task.id}
              title={task.title}
              description={task.description}
              completed={task.completed}
              created_at={task.created_at}
              updated_at={task.updated_at}
              priority={task.priority}
              due_date={task.due_date}
              onToggle={() => onToggleTask?.(task.id)}
              onEdit={() => onEditTask?.(task.id)}
              onDelete={() => onDeleteTask?.(task.id)}
            />
          ))
        ) : (
          <div className="p-8">
            <EmptyState
              title="No tasks found"
              description={emptyStateText}
            />
          </div>
        )}
      </div>
    </div>
  )
}

// TaskListHeader component for custom headers
interface TaskListHeaderProps {
  children: React.ReactNode
  className?: string
}

export const TaskListHeader: React.FC<TaskListHeaderProps> = ({
  children,
  className
}) => {
  return (
    <div className={cn('p-4 border-b border-gray-200 bg-gray-50', className)}>
      {children}
    </div>
  )
}

// TaskListFooter component for pagination or additional controls
interface TaskListFooterProps {
  children: React.ReactNode
  className?: string
}

export const TaskListFooter: React.FC<TaskListFooterProps> = ({
  children,
  className
}) => {
  return (
    <div className={cn('p-4 border-t border-gray-200 bg-gray-50', className)}>
      {children}
    </div>
  )
}

// TaskListGroup component for grouping tasks by date or category
interface TaskListGroupProps {
  title: string
  tasks: Task[]
  onToggleTask?: (id: string | number) => void
  onEditTask?: (id: string | number) => void
  onDeleteTask?: (id: string | number) => void
  className?: string
}

export const TaskListGroup: React.FC<TaskListGroupProps> = ({
  title,
  tasks,
  onToggleTask,
  onEditTask,
  onDeleteTask,
  className
}) => {
  return (
    <div className={cn('border rounded-lg shadow-sm', className)}>
      <div className="p-4 border-b border-gray-200 bg-gray-50">
        <h3 className="font-medium text-gray-900">{title}</h3>
        <p className="text-sm text-gray-500">{tasks.length} tasks</p>
      </div>
      <div className="divide-y divide-gray-200">
        {tasks.map((task) => (
          <TaskItem
            key={task.id}
            id={task.id}
            title={task.title}
            description={task.description}
            completed={task.completed}
            created_at={task.created_at}
            updated_at={task.updated_at}
            priority={task.priority}
            due_date={task.due_date}
            onToggle={() => onToggleTask?.(task.id)}
            onEdit={() => onEditTask?.(task.id)}
            onDelete={() => onDeleteTask?.(task.id)}
          />
        ))}
        {tasks.length === 0 && (
          <div className="p-8 text-center text-gray-500">No tasks in this group</div>
        )}
      </div>
    </div>
  )
};