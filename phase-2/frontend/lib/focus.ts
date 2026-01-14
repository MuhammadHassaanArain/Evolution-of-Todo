// Focus management utilities for accessibility

// Focus trap for modals and dialogs
export function createFocusTrap(element: HTMLElement): () => void {
  if (!element) {
    return () => {}
  }

  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>

  if (focusableElements.length === 0) {
    // If no focusable elements, return early
    return () => {}
  }

  const firstElement = focusableElements[0]
  const lastElement = focusableElements[focusableElements.length - 1]

  const handleKeyDown = (e: KeyboardEvent) => {
    if (e.key !== 'Tab') return

    if (e.shiftKey) {
      // Shift + Tab
      if (document.activeElement === firstElement) {
        lastElement.focus()
        e.preventDefault()
      }
    } else {
      // Tab
      if (document.activeElement === lastElement) {
        firstElement.focus()
        e.preventDefault()
      }
    }
  }

  element.addEventListener('keydown', handleKeyDown)

  // Focus the first element when focus trap is created
  firstElement.focus()

  // Return cleanup function
  return () => {
    element.removeEventListener('keydown', handleKeyDown)
  }
}

// Focus first element in a container
export function focusFirstElement(container: HTMLElement | null): void {
  if (!container) return

  const focusableElements = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>

  const firstElement = focusableElements[0]
  if (firstElement) {
    firstElement.focus()
  }
}

// Focus last element in a container
export function focusLastElement(container: HTMLElement | null): void {
  if (!container) return

  const focusableElements = container.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>

  const lastElement = focusableElements[focusableElements.length - 1]
  if (lastElement) {
    lastElement.focus()
  }
}

// Focus element with selector
export function focusElement(selector: string): boolean {
  const element = document.querySelector<HTMLElement>(selector)
  if (element) {
    element.focus()
    return true
  }
  return false
}

// Focus element by ID
export function focusById(id: string): boolean {
  const element = document.getElementById(id)
  if (element) {
    element.focus()
    return true
  }
  return false
}

// Move focus to next focusable element
export function focusNext(currentElement: HTMLElement): boolean {
  const allFocusable = document.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>

  const currentIndex = Array.prototype.indexOf.call(allFocusable, currentElement)
  const nextIndex = currentIndex + 1

  if (nextIndex < allFocusable.length) {
    allFocusable[nextIndex].focus()
    return true
  }

  return false
}

// Move focus to previous focusable element
export function focusPrevious(currentElement: HTMLElement): boolean {
  const allFocusable = document.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  ) as NodeListOf<HTMLElement>

  const currentIndex = Array.prototype.indexOf.call(allFocusable, currentElement)
  const prevIndex = currentIndex - 1

  if (prevIndex >= 0) {
    allFocusable[prevIndex].focus()
    return true
  }

  return false
}

// Manage focus when content changes (useful for dynamic content)
export function manageFocusOnChange(
  container: HTMLElement,
  callback?: (newFocusElement: HTMLElement) => void
): MutationObserver | null {
  if (!container) return null

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.type === 'childList') {
        // New elements added, potentially need to adjust focus
        if (callback) {
          const newElements = Array.from(mutation.addedNodes).filter(
            (node) => node.nodeType === Node.ELEMENT_NODE
          ) as HTMLElement[]

          if (newElements.length > 0) {
            // Find the first focusable element in the new content
            const firstFocusable = newElements[0]?.querySelector<HTMLElement>(
              'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
            )

            if (firstFocusable) {
              callback(firstFocusable)
            }
          }
        }
      }
    })
  })

  observer.observe(container, {
    childList: true,
    subtree: true,
  })

  return observer
}

// Store and restore focus
export function createFocusRestorer(): { store: () => void; restore: () => boolean } {
  let storedFocus: HTMLElement | null = null

  return {
    store: () => {
      storedFocus = document.activeElement as HTMLElement
    },
    restore: () => {
      if (storedFocus && storedFocus.focus) {
        storedFocus.focus()
        return true
      }
      return false
    },
  }
}

// Check if an element is focusable
export function isFocusable(element: HTMLElement): boolean {
  // Check if element has disabled attribute (for input, button, etc.)
  if ('disabled' in element && (element as HTMLInputElement | HTMLButtonElement).disabled) return false

  // Check if element is visible
  const style = window.getComputedStyle(element)
  if (style.display === 'none' || style.visibility === 'hidden') return false

  // Check tabIndex
  const tabIndex = element.getAttribute('tabindex')
  if (tabIndex === '-1') return false

  // Check if element can receive focus based on its tag
  const focusableTags = ['BUTTON', 'INPUT', 'SELECT', 'TEXTAREA', 'A', 'AREA', 'SUMMARY', 'AUDIO', 'VIDEO']
  if (focusableTags.includes(element.tagName)) {
    if (element.tagName === 'INPUT') {
      return (element as HTMLInputElement).type !== 'hidden'
    }
    return true
  }

  // Check if element has a valid tabIndex
  if (tabIndex !== null) {
    const parsedTabIndex = parseInt(tabIndex, 10)
    return !isNaN(parsedTabIndex) && parsedTabIndex >= -1
  }

  // Check if element has contenteditable
  const contentEditable = element.getAttribute('contenteditable')
  if (contentEditable && contentEditable.toLowerCase() !== 'false') {
    return true
  }

  return false
}

// Get all focusable elements in a container
export function getFocusableElements(container: HTMLElement): HTMLElement[] {
  const allElements = container.querySelectorAll('*')
  return Array.from(allElements).filter((element): element is HTMLElement => {
    return element instanceof HTMLElement && isFocusable(element)
  })
}

// Scroll to element and focus (useful for error states)
export function scrollToAndFocus(selector: string): boolean {
  const element = document.querySelector<HTMLElement>(selector)
  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' })
    element.focus({ preventScroll: true })
    return true
  }
  return false
}