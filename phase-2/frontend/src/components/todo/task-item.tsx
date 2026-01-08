'use client'

import React from 'react'
import { Button } from '../ui/button'
import { cn } from '@/lib/utils'

export interface TaskItemProps {
  id: string | number
  title: string
  description?: string
  completed: boolean
  created_at: string  // Updated to match backend format
  updated_at: string  // Updated to match backend format
  onToggle?: () => void
  onEdit?: () => void
  onDelete?: () => void
  className?: string
  priority?: 'low' | 'medium' | 'high'
  due_date?: string  // Updated to match backend format
}

export const TaskItem: React.FC<TaskItemProps> = ({
  id,
  title,
  description,
  completed,
  created_at,
  updated_at,
  onToggle,
  onEdit,
  onDelete,
  className,
  priority = 'medium',
  due_date,
  ...props
}) => {
  const priorityColors = {
    low: 'border-l-green-500 bg-green-50',
    medium: 'border-l-yellow-500 bg-yellow-50',
    high: 'border-l-red-500 bg-red-50'
  }

  const priorityLabels = {
    low: 'Low Priority',
    medium: 'Medium Priority',
    high: 'High Priority'
  }

  const formatDate = (dateString: string) => {
    // Create a consistent date format that works both server and client side
    const date = new Date(dateString);
    // Use a format that's consistent across environments
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  }

  return (
    <div
      className={cn(
        'border-l-4 p-4 rounded-r-md shadow-sm hover:shadow-md transition-shadow duration-200',
        completed ? 'bg-gray-50 opacity-70' : priorityColors[priority],
        className
      )}
      {...props}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3 flex-1 min-w-0">
          <input
            type="checkbox"
            checked={completed}
            onChange={onToggle}
            className="mt-1 h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
            aria-label={completed ? `Mark "${title}" as incomplete` : `Mark "${title}" as complete`}
          />

          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h3
                className={cn(
                  'text-base font-medium truncate',
                  completed ? 'line-through text-gray-500' : 'text-gray-900'
                )}
              >
                {title}
              </h3>

              <div className="flex items-center space-x-2 ml-2">
                {priority !== 'medium' && (
                  <span
                    className={cn(
                      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
                      priority === 'low'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-red-100 text-red-800'
                    )}
                  >
                    {priority === 'low' ? 'Low' : 'High'}
                  </span>
                )}

                {due_date && (
                  <span
                    className={cn(
                      'text-xs px-2 py-1 rounded',
                      new Date(due_date) < new Date() && !completed
                        ? 'bg-red-100 text-red-800'
                        : 'bg-gray-100 text-gray-800'
                    )}
                  >
                    Due: {formatDate(due_date)}
                  </span>
                )}
              </div>
            </div>

            {description && (
              <p
                className={cn(
                  'mt-1 text-sm truncate',
                  completed ? 'text-gray-400' : 'text-gray-600'
                )}
              >
                {description}
              </p>
            )}

            <div className="mt-2 flex items-center text-xs text-gray-500">
              <span>Created: {formatDate(created_at)}</span>
              {updated_at !== created_at && (
                <span className="ml-3">Updated: {formatDate(updated_at)}</span>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2 ml-4">
          <Button
            variant="outline"
            size="sm"
            onClick={onEdit}
            aria-label={`Edit task "${title}"`}
          >
            Edit
          </Button>
          <Button
            variant="destructive"
            size="sm"
            onClick={onDelete}
            aria-label={`Delete task "${title}"`}
          >
            Delete
          </Button>
        </div>
      </div>
    </div>
  )
}

