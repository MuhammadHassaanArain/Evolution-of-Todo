import React, { forwardRef } from 'react'
import { cn } from '@/lib/utils'

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'destructive'
  size?: 'sm' | 'md' | 'lg'
  isLoading?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  fullWidth?: boolean
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant = 'primary',
      size = 'md',
      isLoading = false,
      leftIcon,
      rightIcon,
      fullWidth = false,
      children,
      disabled,
      ...props
    },
    ref
  ) => {
    const baseClasses = cn(
      'inline-flex items-center justify-center rounded-md font-medium transition-all duration-200',
      'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2',
      'disabled:pointer-events-none disabled:opacity-50',
      'outline-none', // Remove default outline for better focus management
      fullWidth ? 'w-full' : '',
      // Visual feedback states
      'hover:shadow-sm active:scale-[0.98] active:shadow-inner',
      // Transition properties for visual feedback
      'transition-colors transition-transform transition-shadow'
    )

    const variantClasses = {
      primary: cn(
        'bg-indigo-600 text-white hover:bg-indigo-700',
        'focus-visible:ring-indigo-500'
      ),
      secondary: cn(
        'bg-gray-200 text-gray-900 hover:bg-gray-300',
        'focus-visible:ring-gray-500'
      ),
      outline: cn(
        'border border-gray-300 bg-transparent text-gray-900 hover:bg-gray-100',
        'focus-visible:ring-gray-500'
      ),
      ghost: cn(
        'hover:bg-gray-100 text-gray-700 hover:text-gray-900',
        'focus-visible:ring-gray-500'
      ),
      link: cn(
        'text-indigo-600 underline-offset-4 hover:underline',
        'focus-visible:ring-indigo-500'
      ),
      destructive: cn(
        'bg-red-600 text-white hover:bg-red-700',
        'focus-visible:ring-red-500'
      ),
    }

    const sizeClasses = {
      sm: 'h-9 px-3 text-sm',
      md: 'h-10 px-4 py-2 text-sm',
      lg: 'h-12 px-8 text-base',
    }

    const computedClassName = cn(
      baseClasses,
      variantClasses[variant],
      sizeClasses[size],
      className
    )

    return (
      <button
        ref={ref}
        className={computedClassName}
        disabled={disabled || isLoading}
        aria-busy={isLoading}
        aria-disabled={disabled || isLoading}
        {...props}
      >
        {isLoading ? (
          <span className="flex items-center">
            <Spinner className="mr-2" aria-hidden="true" />
            <span aria-live="polite">Loading...</span>
          </span>
        ) : (
          <>
            {leftIcon && !isLoading && <span className="mr-2" aria-hidden="true">{leftIcon}</span>}
            {children}
            {rightIcon && !isLoading && <span className="ml-2" aria-hidden="true">{rightIcon}</span>}
          </>
        )}
      </button>
    )
  }
)

Button.displayName = 'Button'

// Spinner component for loading states
interface SpinnerProps {
  className?: string
}

const Spinner = ({ className }: SpinnerProps) => {
  return (
    <svg
      className={cn('animate-spin h-4 w-4 text-current', className)}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      ></circle>
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      ></path>
    </svg>
  )
}

Spinner.displayName = 'Spinner'