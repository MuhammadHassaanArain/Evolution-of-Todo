'use client'

import React from 'react'
import { Button } from '../ui/button'
import { cn } from '@/lib/utils'



export interface EmptyStateProps {
  title?: string
  description?: string
  actionText?: string
  onAction?: () => void
  icon?: React.ReactNode
  className?: string
  showAction?: boolean
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = 'No tasks yet',
  description = 'Get started by creating your first task. You\'ll see it appear here once added.',
  actionText = 'Create Task',
  onAction,
  icon,
  className,
  showAction = true,
  ...props
}) => {
  return (
    <div
      className={cn(
        'flex flex-col items-center justify-center py-12 px-4 text-center',
        className
      )}
      {...props}
    >
      <div className="mb-6 flex flex-col items-center">
        {icon ? (
          <div className="mb-4 text-gray-400">{icon}</div>
        ) : (
          <div className="mb-4 text-gray-400">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-16 w-16"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={1.5}
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              />
            </svg>
          </div>
        )}

        <h3 className="text-lg font-medium text-gray-900 mb-1">{title}</h3>
        <p className="text-gray-500 max-w-md">{description}</p>
      </div>

      {showAction && onAction && (
        <Button
          onClick={onAction}
          className="mt-4"
          aria-label={`Create new task`}
        >
          {actionText}
        </Button>
      )}
    </div>
  )
}