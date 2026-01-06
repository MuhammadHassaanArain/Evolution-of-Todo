'use client'

import React, { useState, useCallback } from 'react'
import { Button } from '../ui/button'
import { Input, Textarea } from '../ui/input'
import { Select, SelectItem } from '../ui/select'
import { cn } from '../../lib/utils'

export interface TaskFormValues {
  title: string
  description?: string
  priority: 'low' | 'medium' | 'high'
  dueDate?: string
}

export interface TaskFormProps {
  initialValues?: TaskFormValues
  onSubmit: (values: TaskFormValues) => Promise<void> // Changed to async
  onCancel?: () => void
  submitText?: string
  className?: string
  isSubmitting?: boolean
}

export const TaskForm: React.FC<TaskFormProps> = React.memo(({
  initialValues = {
    title: '',
    description: '',
    priority: 'medium',
    dueDate: ''
  },
  onSubmit,
  onCancel,
  submitText = 'Save Task',
  className,
  isSubmitting = false,
  ...props
}) => {
  const [formData, setFormData] = useState<TaskFormValues>(initialValues)
  const [errors, setErrors] = useState<Partial<TaskFormValues>>({})
  const [submitError, setSubmitError] = useState<string | null>(null)

  const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))

    // Clear error when user starts typing
    if (errors[name as keyof TaskFormValues]) {
      setErrors(prev => ({
        ...prev,
        [name]: undefined
      }))
    }

    // Clear submit error when user starts typing
    if (submitError) {
      setSubmitError(null)
    }
  }, [errors, submitError])

  const handlePriorityChange = useCallback((value: string) => {
    setFormData(prev => ({
      ...prev,
      priority: value as 'low' | 'medium' | 'high'
    }))

    // Clear error when user selects a value
    if (errors.priority) {
      setErrors(prev => ({
        ...prev,
        priority: undefined
      }))
    }

    // Clear submit error when user changes priority
    if (submitError) {
      setSubmitError(null)
    }
  }, [errors, submitError])

  const handleDateChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      dueDate: e.target.value
    }))

    // Clear error when user selects a date
    if (errors.dueDate) {
      setErrors(prev => ({
        ...prev,
        dueDate: undefined
      }))
    }

    // Clear submit error when user changes date
    if (submitError) {
      setSubmitError(null)
    }
  }, [errors, submitError])

  const validate = useCallback((): boolean => {
    const newErrors: Partial<TaskFormValues> = {}

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required'
    } else if (formData.title.trim().length < 3) {
      newErrors.title = 'Title must be at least 3 characters'
    }

    if (formData.dueDate && new Date(formData.dueDate) < new Date()) {
      newErrors.dueDate = 'Due date cannot be in the past'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }, [formData])

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault()

    if (validate()) {
      try {
        setSubmitError(null)
        await onSubmit(formData)
        // Clear form after successful submission
        if (!initialValues || !initialValues.hasOwnProperty('id')) { // Only clear if creating new task
          setFormData({
            title: '',
            description: '',
            priority: 'medium',
            dueDate: ''
          })
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : 'An error occurred'
        setSubmitError(errorMessage)
      }
    }
  }, [validate, onSubmit, formData, initialValues])

  return (
    <form onSubmit={handleSubmit} className={cn('space-y-4', className)} {...props}>
      <Input
        label="Title *"
        id="title"
        name="title"
        value={formData.title}
        onChange={handleChange}
        placeholder="Enter task title"
        error={errors.title}
        required
      />

      <Textarea
        label="Description"
        id="description"
        name="description"
        value={formData.description || ''}
        onChange={handleChange}
        placeholder="Enter task description (optional)"
        rows={3}
      />

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Select
          label="Priority"
          value={formData.priority}
          onValueChange={handlePriorityChange}
          error={errors.priority}
        >
          <SelectItem value="low">Low Priority</SelectItem>
          <SelectItem value="medium">Medium Priority</SelectItem>
          <SelectItem value="high">High Priority</SelectItem>
        </Select>

        <Input
          label="Due Date"
          id="dueDate"
          name="dueDate"
          type="date"
          value={formData.dueDate || ''}
          onChange={handleDateChange}
          error={errors.dueDate}
        />
      </div>

      {submitError && (
        <div className="text-sm text-red-600 p-2 bg-red-50 rounded-md">
          {submitError}
        </div>
      )}

      <div className="flex justify-end space-x-3 pt-2">
        {onCancel && (
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            disabled={isSubmitting}
            aria-label="Cancel task form"
          >
            Cancel
          </Button>
        )}
        <Button
          type="submit"
          disabled={isSubmitting}
          aria-label="Save task"
        >
          {isSubmitting ? 'Saving...' : submitText}
        </Button>
      </div>
    </form>
  )
})

TaskForm.displayName = 'TaskForm'