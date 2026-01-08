import React, { forwardRef } from 'react'
import { cn } from '../../lib/utils'

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string
  error?: string
  helperText?: string
  required?: boolean
  leftIcon?: React.ReactNode
  rightIcon?: React.ReactNode
  variant?: 'default' | 'filled' | 'outline'
  fullWidth?: boolean
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      type,
      label,
      error,
      helperText,
      required,
      leftIcon,
      rightIcon,
      variant = 'default',
      fullWidth = false,
      id,
      ...props
    },
    ref
  ) => {
    const hasError = !!error

    // Generate a unique ID if none is provided
    const inputId = id || `input-${Math.random().toString(36).substr(2, 9)}`

    // Base classes for the input
    const baseClasses = [
      'flex h-10 w-full rounded-md border px-3 py-2 text-sm',
      'ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium',
      'placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
      'disabled:cursor-not-allowed disabled:opacity-50',
      fullWidth ? 'w-full' : '',
      variant === 'outline' ? 'border-input bg-transparent' : '',
      variant === 'filled' ? 'border-transparent bg-secondary' : '',
      hasError ? 'border-red-500 focus-visible:ring-red-500' : 'border-input',
    ]

    const inputClasses = cn(baseClasses.filter(Boolean), className)

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label
            htmlFor={inputId}
            className={cn(
              'block text-sm font-medium mb-1',
              hasError ? 'text-red-700' : 'text-gray-700'
            )}
          >
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}

        <div className="relative">
          {leftIcon && (
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              {leftIcon}
            </div>
          )}

          <input
            id={inputId}
            type={type}
            ref={ref}
            required={required}
            aria-invalid={hasError}
            aria-describedby={helperText || hasError ? `${inputId}-helper-text` : undefined}
            className={inputClasses}
            style={{
              paddingLeft: leftIcon ? '2.5rem' : undefined,
              paddingRight: rightIcon ? '2.5rem' : undefined,
            }}
            {...props}
          />

          {rightIcon && (
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
              {rightIcon}
            </div>
          )}
        </div>

        {(helperText || hasError) && (
          <p
            id={`${inputId}-helper-text`}
            className={cn(
              'mt-1 text-sm',
              hasError ? 'text-red-600' : 'text-gray-500'
            )}
            aria-live="polite"
          >
            {hasError ? error : helperText}
          </p>
        )}
      </div>
    )
  }
)

Input.displayName = 'Input'

// Textarea component with similar accessibility features
export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string
  error?: string
  helperText?: string
  required?: boolean
  fullWidth?: boolean
}

export const Textarea = forwardRef<HTMLTextAreaElement, TextareaProps>(
  (
    { className, label, error, helperText, required, fullWidth = false, id, ...props },
    ref
  ) => {
    const hasError = !!error
    const textareaId = id || `textarea-${Math.random().toString(36).substr(2, 9)}`

    return (
      <div className={fullWidth ? 'w-full' : ''}>
        {label && (
          <label
            htmlFor={textareaId}
            className={cn(
              'block text-sm font-medium mb-1',
              hasError ? 'text-red-700' : 'text-gray-700'
            )}
          >
            {label}
            {required && <span className="text-red-500 ml-1">*</span>}
          </label>
        )}

        <textarea
          id={textareaId}
          ref={ref}
          required={required}
          aria-invalid={hasError}
          aria-describedby={helperText || hasError ? `${textareaId}-helper-text` : undefined}
          className={cn(
            'flex min-h-[80px] w-full rounded-md border border-input bg-transparent px-3 py-2 text-sm',
            'ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
            'disabled:cursor-not-allowed disabled:opacity-50',
            fullWidth ? 'w-full' : '',
            hasError ? 'border-red-500 focus-visible:ring-red-500' : '',
            className
          )}
          {...props}
        />

        {(helperText || hasError) && (
          <p
            id={`${textareaId}-helper-text`}
            className={cn(
              'mt-1 text-sm',
              hasError ? 'text-red-600' : 'text-gray-500'
            )}
            aria-live="polite"
          >
            {hasError ? error : helperText}
          </p>
        )}
      </div>
    )
  }
)

Textarea.displayName = 'Textarea'