'use client'

import React from 'react'
import { Button } from '../ui/button'
import { cn } from '../../lib/utils'

export interface ConfirmationDialogProps {
  isOpen: boolean
  title?: string
  message?: string
  confirmText?: string
  cancelText?: string
  onConfirm: () => void
  onCancel: () => void
  className?: string
}

export const ConfirmationDialog: React.FC<ConfirmationDialogProps> = ({
  isOpen,
  title = 'Confirm Action',
  message = 'Are you sure you want to proceed?',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  onConfirm,
  onCancel,
  className,
  ...props
}) => {
  if (!isOpen) {
    return null
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black bg-opacity-50"
      role="dialog"
      aria-modal="true"
      aria-labelledby="confirmation-dialog-title"
    >
      <div
        className={cn(
          'bg-white rounded-lg shadow-xl max-w-md w-full p-6 space-y-4',
          className
        )}
        {...props}
      >
        <div className="flex items-start">
          <div className="ml-0 flex-1">
            <h3
              id="confirmation-dialog-title"
              className="text-lg font-medium text-gray-900"
            >
              {title}
            </h3>
            <div className="mt-2">
              <p className="text-sm text-gray-500">
                {message}
              </p>
            </div>
          </div>
        </div>

        <div className="flex justify-end space-x-3 mt-4">
          <Button
            type="button"
            variant="outline"
            onClick={onCancel}
            className="px-4 py-2"
          >
            {cancelText}
          </Button>
          <Button
            type="button"
            variant="destructive"
            onClick={onConfirm}
            className="px-4 py-2"
          >
            {confirmText}
          </Button>
        </div>
      </div>
    </div>
  )
}