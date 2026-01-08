'use client'

import React, { useEffect, useState, useCallback, useMemo } from 'react'
import { cn } from '@/lib/utils'

export type FeedbackType = 'success' | 'error' | 'info' | 'warning'

export interface TaskFeedbackProps {
  message: string
  type?: FeedbackType
  visible?: boolean
  duration?: number
  className?: string
  onClose?: () => void
}

export const TaskFeedback: React.FC<TaskFeedbackProps> = React.memo(({
  message,
  type = 'info',
  visible = true,
  duration = 0,
  className,
  onClose,
  ...props
}) => {
  const [isVisible, setIsVisible] = useState(visible)

  useEffect(() => {
    setIsVisible(visible)
  }, [visible])

  useEffect(() => {
    if (duration > 0 && isVisible) {
      const timer = setTimeout(() => {
        setIsVisible(false)
        onClose?.()
      }, duration)

      return () => clearTimeout(timer)
    }
  }, [duration, isVisible, onClose])

  const handleClose = useCallback(() => {
    setIsVisible(false)
    onClose?.()
  }, [onClose])

  if (!isVisible) {
    return null
  }

  const typeStyles = useMemo(() => ({
    success: 'bg-green-100 text-green-800 border-green-200',
    error: 'bg-red-100 text-red-800 border-red-200',
    info: 'bg-blue-100 text-blue-800 border-blue-200',
    warning: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  }), [])

  return (
    <div
      className={cn(
        'flex items-center p-4 rounded-lg border border-b-4 shadow-sm transition-all duration-300',
        typeStyles[type],
        className
      )}
      role="alert"
      {...props}
    >
      <div className="flex-1">
        <p className="text-sm font-medium">{message}</p>
      </div>
      {duration === 0 && (
        <button
          onClick={handleClose}
          className="ml-4 text-current hover:opacity-75 focus:outline-none focus:ring-2 focus:ring-current rounded-full p-1"
          aria-label="Close notification"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-5 w-5"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      )}
    </div>
  )
})

TaskFeedback.displayName = 'TaskFeedback'

// Hook to manage feedback state
export interface UseTaskFeedbackReturn {
  feedback: {
    message: string
    type: FeedbackType
  } | null
  showFeedback: (message: string, type?: FeedbackType, duration?: number) => void
  hideFeedback: () => void
}

export const useTaskFeedback = (): UseTaskFeedbackReturn => {
  const [feedback, setFeedback] = useState<{
    message: string
    type: FeedbackType
  } | null>(null)

  const showFeedback = useCallback((
    message: string,
    type: FeedbackType = 'info',
    duration = 3000
  ) => {
    setFeedback({ message, type })

    if (duration > 0) {
      setTimeout(() => {
        setFeedback(null)
      }, duration)
    }
  }, [])

  const hideFeedback = useCallback(() => {
    setFeedback(null)
  }, [])

  return {
    feedback,
    showFeedback,
    hideFeedback,
  }
}