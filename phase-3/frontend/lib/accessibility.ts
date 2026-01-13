// Accessibility utilities and ARIA helpers

// Focus management utilities
export function focusFirstElement(parent: HTMLElement | null) {
  if (!parent) return

  const focusableElements = parent.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>

  const firstFocusable = focusableElements[0]
  if (firstFocusable) {
    firstFocusable.focus()
  }
}

// Trap focus within an element (useful for modals)
export function trapFocus(
  element: HTMLElement | null,
  callback?: (event: KeyboardEvent) => void
) {
  if (!element) return

  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>

  const firstElement = focusableElements[0]
  const lastElement = focusableElements[focusableElements.length - 1]

  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key !== 'Tab') {
      if (callback) callback(event)
      return
    }

    if (event.shiftKey) {
      // Shift + Tab
      if (document.activeElement === firstElement) {
        lastElement.focus()
        event.preventDefault()
      }
    } else {
      // Tab
      if (document.activeElement === lastElement) {
        firstElement.focus()
        event.preventDefault()
      }
    }
  }

  element.addEventListener('keydown', handleKeyDown)

  // Return cleanup function
  return () => {
    element.removeEventListener('keydown', handleKeyDown)
  }
}

// Generate unique IDs for accessibility attributes
let idCounter = 0
export function generateId(prefix: string = 'id'): string {
  idCounter++
  return `${prefix}-${idCounter}`
}

// Announce text to screen readers
export function announceToScreenReader(message: string) {
  const announcement = document.createElement('div')
  announcement.setAttribute('aria-live', 'polite')
  announcement.setAttribute('aria-atomic', 'true')
  announcement.className = 'sr-only'
  announcement.textContent = message

  document.body.appendChild(announcement)

  // Remove after a delay
  setTimeout(() => {
    document.body.removeChild(announcement)
  }, 1000)
}

// Check if user prefers reduced motion
export function prefersReducedMotion(): boolean {
  if (typeof window === 'undefined') return false
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

// Check if user prefers dark mode
export function prefersDarkMode(): boolean {
  if (typeof window === 'undefined') return false
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

// ARIA attributes for common components
export const ARIA = {
  // Modal attributes
  modal: {
    role: 'dialog',
    'aria-modal': 'true',
  } as const,

  // Alert attributes
  alert: {
    role: 'alert',
  } as const,

  // Alert dialog attributes
  alertDialog: {
    role: 'alertdialog',
    'aria-modal': 'true',
  } as const,

  // Live region attributes
  liveRegion: {
    'aria-live': 'polite',
    'aria-atomic': 'true',
    className: 'sr-only',
  } as const,

  // Skip link attributes
  skipLink: {
    className: 'sr-only focus:not-sr-only focus:bg-white focus:text-black focus:p-4 focus:z-50',
    href: '#main-content',
  } as const,
}

// Utility to get ARIA-compliant attributes for common states
export function getAriaAttributes({
  disabled,
  invalid,
  required,
  expanded,
  selected,
  pressed,
  hidden,
}: {
  disabled?: boolean
  invalid?: boolean
  required?: boolean
  expanded?: boolean
  selected?: boolean
  pressed?: boolean
  hidden?: boolean
}): Record<string, string | boolean> {
  const attrs: Record<string, string | boolean> = {}

  if (disabled !== undefined) attrs['aria-disabled'] = disabled
  if (invalid !== undefined) attrs['aria-invalid'] = invalid
  if (required !== undefined) attrs['aria-required'] = required
  if (expanded !== undefined) attrs['aria-expanded'] = expanded
  if (selected !== undefined) attrs['aria-selected'] = selected
  if (pressed !== undefined) attrs['aria-pressed'] = pressed
  if (hidden !== undefined) attrs['aria-hidden'] = hidden

  return attrs
}