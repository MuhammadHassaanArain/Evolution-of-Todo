import React, { createContext, useContext, useState, ReactNode } from 'react'
import { Button } from './button'
import { Input, Textarea } from './input'
import { cn } from '@/lib/utils'
// Form context for sharing form state
interface FormContextProps {
  formData: Record<string, any>
  errors: Record<string, string>
  touched: Record<string, boolean>
  setFormData: React.Dispatch<React.SetStateAction<Record<string, any>>>
  setErrors: React.Dispatch<React.SetStateAction<Record<string, string>>>
  setTouched: React.Dispatch<React.SetStateAction<Record<string, boolean>>>
  validateField: (name: string, value: any) => void
  submit: () => void
  isSubmitting: boolean
}

const FormContext = createContext<FormContextProps | undefined>(undefined)

export const useForm = (): FormContextProps => {
  const context = useContext(FormContext)
  if (!context) {
    throw new Error('useForm must be used within a FormProvider')
  }
  return context
}

// Form provider component
interface FormProviderProps {
  children: ReactNode
  onSubmit: (data: Record<string, any>) => void
  initialValues?: Record<string, any>
  validate?: (values: Record<string, any>) => Record<string, string>
}

export const FormProvider: React.FC<FormProviderProps> = ({
  children,
  onSubmit,
  initialValues = {},
  validate
}) => {
  const [formData, setFormData] = useState<Record<string, any>>(initialValues)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [touched, setTouched] = useState<Record<string, boolean>>({})
  const [isSubmitting, setIsSubmitting] = useState(false)

  const validateField = (name: string, value: any) => {
    if (validate) {
      const fieldErrors = validate({ ...formData, [name]: value })
      setErrors(fieldErrors)
      return fieldErrors[name]
    }
    return undefined
  }

  const submit = async () => {
    setIsSubmitting(true)

    // Mark all fields as touched
    const allTouched = Object.keys(formData).reduce((acc, key) => {
      acc[key] = true
      return acc
    }, {} as Record<string, boolean>)
    setTouched(allTouched)

    // Validate all fields
    if (validate) {
      const validationErrors = validate(formData)
      setErrors(validationErrors)

      // If there are validation errors, stop submission
      if (Object.keys(validationErrors).length > 0) {
        setIsSubmitting(false)
        return
      }
    }

    try {
      await onSubmit(formData)
    } catch (error) {
      console.error('Form submission error:', error)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <FormContext.Provider
      value={{
        formData,
        errors,
        touched,
        setFormData,
        setErrors,
        setTouched,
        validateField,
        submit,
        isSubmitting
      }}
    >
      {children}
    </FormContext.Provider>
  )
}

// Form component
interface FormProps {
  children: ReactNode
  onSubmit: (data: Record<string, any>) => void
  className?: string
  initialValues?: Record<string, any>
  validate?: (values: Record<string, any>) => Record<string, string>
}

export const Form: React.FC<FormProps> = ({
  children,
  onSubmit,
  className,
  initialValues = {},
  validate
}) => {
  const { submit } = useForm();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    submit();
  };

  return (
    <FormProvider onSubmit={onSubmit} initialValues={initialValues} validate={validate}>
      <form
        onSubmit={handleSubmit}
        className={cn(className)}
        noValidate
      >
        {children}
      </form>
    </FormProvider>
  )
}

// Form field component
interface FormFieldProps {
  name: string
  label?: string
  required?: boolean
  helperText?: string
  validate?: (value: any) => string | undefined
  children: (props: {
    value: any
    onChange: (value: any) => void
    onBlur: () => void
    error: string | undefined
    touched: boolean
  }) => ReactNode
}

export const FormField: React.FC<FormFieldProps> = ({ name, label, required, helperText, validate, children }) => {
  const { formData, errors, touched, setFormData, setTouched, setErrors, validateField } = useForm()

  const handleChange = (value: any) => {
    setFormData(prev => ({ ...prev, [name]: value }))

    // Validate field on change if validation function is provided
    if (validate) {
      const error = validate(value)
      if (error) {
        setErrors(prev => ({ ...prev, [name]: error }))
      } else {
        setErrors(prev => {
          const newErrors = { ...prev }
          delete newErrors[name]
          return newErrors
        })
      }
    } else if (validateField) {
      validateField(name, value)
    }
  }

  const handleBlur = () => {
    setTouched(prev => ({ ...prev, [name]: true }))
  }

  const error = errors[name]
  const isTouched = touched[name] || false

  return children({
    value: formData[name],
    onChange: handleChange,
    onBlur: handleBlur,
    error: isTouched ? error : undefined,
    touched: isTouched
  })
}

// Pre-built input field component
interface FormInputProps {
  name: string
  label: string
  type?: string
  placeholder?: string
  required?: boolean
  validate?: (value: any) => string | undefined
}

export const FormInput: React.FC<FormInputProps> = ({ name, label, type = 'text', placeholder, required, validate }) => {
  return (
    <FormField
      name={name}
      label={label}
      required={required}
      validate={validate}
    >
      {({ value, onChange, onBlur, error, touched }) => (
        <Input
          type={type}
          label={label}
          placeholder={placeholder}
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          onBlur={onBlur}
          error={touched ? error : undefined}
          required={required}
        />
      )}
    </FormField>
  )
}

// Pre-built textarea field component
interface FormTextareaProps {
  name: string
  label: string
  placeholder?: string
  required?: boolean
  validate?: (value: any) => string | undefined
}

export const FormTextarea: React.FC<FormTextareaProps> = ({ name, label, placeholder, required, validate }) => {
  return (
    <FormField
      name={name}
      label={label}
      required={required}
      validate={validate}
    >
      {({ value, onChange, onBlur, error, touched }) => (
        <Textarea
          label={label}
          placeholder={placeholder}
          value={value || ''}
          onChange={(e) => onChange(e.target.value)}
          onBlur={onBlur}
          error={touched ? error : undefined}
          required={required}
        />
      )}
    </FormField>
  )
}

// Form submit button component
interface FormSubmitButtonProps {
  children: ReactNode
  className?: string
}

export const FormSubmitButton: React.FC<FormSubmitButtonProps> = ({ children, className }) => {
  const { isSubmitting } = useForm()

  return (
    <Button
      type="submit"
      disabled={isSubmitting}
      className={className}
      isLoading={isSubmitting}
    >
      {children}
    </Button>
  )
}

// Form error display component
interface FormErrorProps {
  fieldName?: string
  className?: string
}

export const FormError: React.FC<FormErrorProps> = ({ fieldName, className }) => {
  const { errors, touched } = useForm()

  // If fieldName is provided, show error for specific field
  if (fieldName) {
    if (touched[fieldName] && errors[fieldName]) {
      return (
        <div className={cn('text-red-600 text-sm mt-1', className)} role="alert" aria-live="polite">
          {errors[fieldName]}
        </div>
      )
    }
    return null
  }

  // Otherwise, show all form errors
  const allErrors = Object.entries(errors).filter(([field]) => touched[field])

  if (allErrors.length === 0) {
    return null
  }

  return (
    <div className={cn('bg-red-50 border border-red-200 rounded-md p-4 mb-4', className)}>
      <h3 className="text-red-800 font-medium mb-2">Please correct the following errors:</h3>
      <ul className="list-disc list-inside text-red-600 text-sm space-y-1">
        {allErrors.map(([field, error]) => (
          <li key={field}>{field}: {error}</li>
        ))}
      </ul>
    </div>
  )
}