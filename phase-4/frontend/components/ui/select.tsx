import React from 'react'
import { cn } from '../../lib/utils'

export interface SelectProps {
  children: React.ReactNode
  value?: string
  onValueChange?: (value: string) => void
  className?: string
  disabled?: boolean
  required?: boolean
  label?: string
  error?: string
  helperText?: string
  name?: string
}

export interface SelectItemProps {
  value: string
  children: React.ReactNode
  className?: string
}

// Main Select component
export const Select: React.FC<SelectProps> = ({
  children,
  value,
  onValueChange,
  className,
  disabled = false,
  required = false,
  label,
  error,
  helperText,
  name,
  ...props
}) => {
  const hasError = !!error
  const selectId = `select-${Math.random().toString(36).substr(2, 9)}`

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (!disabled && onValueChange) {
      onValueChange(e.target.value)
    }
  }

  return (
    <div className={className}>
      {label && (
        <label
          htmlFor={selectId}
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
        <select
          id={selectId}
          name={name}
          value={value}
          onChange={handleChange}
          disabled={disabled}
          required={required}
          aria-invalid={hasError}
          aria-describedby={helperText || hasError ? `${selectId}-helper-text` : undefined}
          className={cn(
            'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm',
            'border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2',
            'appearance-none bg-white',
            hasError ? 'border-red-500' : 'border-gray-300',
            disabled ? 'bg-gray-100 cursor-not-allowed' : '',
            'pr-10'
          )}
        >
          {children}
        </select>
        <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2">
          <svg className="h-4 w-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
        </div>
      </div>

      {(helperText || hasError) && (
        <p
          id={`${selectId}-helper-text`}
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

export const SelectItem: React.FC<SelectItemProps> = ({ value, children, className }) => {
  return (
    <option value={value} className={className}>
      {children}
    </option>
  )
}