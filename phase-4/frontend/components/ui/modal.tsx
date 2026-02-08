import React, { useEffect, useRef, ReactNode } from 'react'
import { createPortal } from 'react-dom'
import { cn } from '../../lib/utils'
import { createFocusTrap, focusFirstElement } from '../../lib/focus'

export interface ModalProps {
  isOpen: boolean
  onClose: () => void
  children: ReactNode
  title?: string
  description?: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  variant?: 'default' | 'alert' | 'confirmation'
  closeOnEscape?: boolean
  closeOnOutsideClick?: boolean
  showCloseButton?: boolean
  className?: string
  role?: 'dialog' | 'alertdialog'
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  children,
  title,
  description,
  size = 'md',
  variant = 'default',
  closeOnEscape = true,
  closeOnOutsideClick = true,
  showCloseButton = true,
  className,
  role = 'dialog'
}) => {
  const modalRef = useRef<HTMLDivElement>(null)
  const containerRef = useRef<HTMLDivElement>(null)

  // Handle keyboard events
  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && closeOnEscape) {
        onClose()
      }
    }

    const handleClickOutside = (e: MouseEvent) => {
      if (
        containerRef.current &&
        !containerRef.current.contains(e.target as Node) &&
        closeOnOutsideClick
      ) {
        onClose()
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    document.addEventListener('mousedown', handleClickOutside)

    // Prevent scrolling of background when modal is open
    document.body.style.overflow = 'hidden'

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.removeEventListener('mousedown', handleClickOutside)
      document.body.style.overflow = ''
    }
  }, [isOpen, onClose, closeOnEscape, closeOnOutsideClick])

  // Focus management
  useEffect(() => {
    if (isOpen && modalRef.current) {
      // Create focus trap
      const cleanup = createFocusTrap(modalRef.current)

      // Focus first element in modal
      focusFirstElement(modalRef.current)

      return cleanup
    }
  }, [isOpen])

  // Size classes
  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
    xl: 'max-w-xl',
    '2xl': 'max-w-2xl'
  }

  // Variant classes
  const variantClasses = {
    default: 'bg-white',
    alert: 'bg-red-50 border border-red-200',
    confirmation: 'bg-yellow-50 border border-yellow-200'
  }

  // Render nothing if modal is not open
  if (!isOpen) return null

  // Modal content
  const modalContent = (
    <div
      ref={containerRef}
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50"
      aria-modal="true"
      aria-labelledby={title ? 'modal-title' : undefined}
      aria-describedby={description ? 'modal-description' : undefined}
      role={role}
    >
      <div
        ref={modalRef}
        className={cn(
          'relative rounded-lg shadow-xl w-full',
          sizeClasses[size],
          variantClasses[variant],
          className
        )}
        tabIndex={-1}
      >
        {/* Modal header */}
        {(title || showCloseButton) && (
          <div className="flex items-center justify-between p-4 border-b">
            {title && (
              <h2
                id="modal-title"
                className={cn(
                  'text-lg font-semibold',
                  variant === 'alert' ? 'text-red-800' :
                  variant === 'confirmation' ? 'text-yellow-800' : 'text-gray-900'
                )}
              >
                {title}
              </h2>
            )}
            {showCloseButton && (
              <button
                onClick={onClose}
                className={cn(
                  'text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 rounded-full p-1',
                  variant === 'alert' ? 'hover:text-red-500' :
                  variant === 'confirmation' ? 'hover:text-yellow-500' : ''
                )}
                aria-label="Close modal"
              >
                <svg
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            )}
          </div>
        )}

        {/* Modal description */}
        {description && (
          <div className="px-4 pt-2 pb-1">
            <p
              id="modal-description"
              className={cn(
                'text-sm',
                variant === 'alert' ? 'text-red-700' :
                variant === 'confirmation' ? 'text-yellow-700' : 'text-gray-500'
              )}
            >
              {description}
            </p>
          </div>
        )}

        {/* Modal body */}
        <div className="p-4">
          {children}
        </div>

        {/* Focus sentinel to help with focus trapping */}
        <div tabIndex={0} aria-hidden="true" className="outline-none" />
      </div>
    </div>
  )

  // Render modal in portal
  return createPortal(modalContent, document.body)
}

// Modal header component for more complex headers
export const ModalHeader: React.FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div className="flex items-center justify-between p-4 border-b">
      {children}
    </div>
  )
}

// Modal body component
export const ModalBody: React.FC<{ children: ReactNode }> = ({ children }) => {
  return <div className="p-4">{children}</div>
}

// Modal footer component
export const ModalFooter: React.FC<{ children: ReactNode }> = ({ children }) => {
  return (
    <div className="flex justify-end p-4 border-t space-x-3">
      {children}
    </div>
  )
}

// Confirm modal component for confirmation dialogs
export interface ConfirmModalProps {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
  title: string
  description?: string
  confirmLabel?: string
  cancelLabel?: string
  confirmVariant?: 'primary' | 'destructive'
}

export const ConfirmModal: React.FC<ConfirmModalProps> = ({
  isOpen,
  onClose,
  onConfirm,
  title,
  description,
  confirmLabel = 'Confirm',
  cancelLabel = 'Cancel',
  confirmVariant = 'destructive'
}) => {
  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={title}
      description={description}
      variant="confirmation"
      role="alertdialog"
    >
      <ModalFooter>
        <button
          onClick={onClose}
          className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          {cancelLabel}
        </button>
        <button
          onClick={onConfirm}
          className={cn(
            'px-4 py-2 text-sm font-medium text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2',
            confirmVariant === 'destructive'
              ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500'
              : 'bg-indigo-600 hover:bg-indigo-700 focus:ring-indigo-500'
          )}
        >
          {confirmLabel}
        </button>
      </ModalFooter>
    </Modal>
  )
}