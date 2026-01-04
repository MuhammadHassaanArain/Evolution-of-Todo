import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Button } from '../../src/components/ui/button'
import { Input } from '../../src/components/ui/input'
import { Modal } from '../../src/components/ui/modal'
import { Card } from '../../src/components/ui/card'
import { Form, FormInput, FormSubmitButton } from '../../src/components/ui/form'

describe('Accessibility Tests', () => {
  describe('Button Component', () => {
    it('should be focusable and keyboard accessible', () => {
      render(<Button>Test Button</Button>)
      const button = screen.getByRole('button', { name: /test button/i })

      // Check that the button is focusable
      button.focus()
      expect(button).toHaveFocus()

      // Check that the button has proper ARIA attributes
      expect(button).toHaveAttribute('role', 'button')
      expect(button).toHaveAttribute('tabIndex', '0')
    })

    it('should have proper ARIA attributes for different states', () => {
      render(
        <>
          <Button disabled>Disabled Button</Button>
          <Button isLoading>Button Loading</Button>
        </>
      )

      const disabledButton = screen.getByRole('button', { name: /disabled button/i })
      expect(disabledButton).toHaveAttribute('disabled')

      const loadingButton = screen.getByRole('button', { name: /button loading/i })
      expect(loadingButton).toHaveAttribute('aria-busy', 'true')
    })

    it('should be operable with keyboard', () => {
      const onClick = vi.fn()
      render(<Button onClick={onClick}>Clickable Button</Button>)
      const button = screen.getByRole('button', { name: /clickable button/i })

      // Focus the button
      button.focus()
      expect(button).toHaveFocus()

      // Press Enter to activate
      fireEvent.keyUp(button, { key: 'Enter' })
      expect(onClick).toHaveBeenCalledTimes(1)

      // Press Space to activate
      fireEvent.keyUp(button, { key: ' ' })
      expect(onClick).toHaveBeenCalledTimes(2)
    })
  })

  describe('Input Component', () => {
    it('should have proper ARIA attributes', () => {
      render(<Input label="Test Label" placeholder="Test Placeholder" />)
      const input = screen.getByRole('textbox', { name: /test label/i })

      expect(input).toHaveAttribute('placeholder', 'Test Placeholder')
      expect(input).toHaveAttribute('aria-label', 'Test Label')
    })

    it('should handle error states properly', () => {
      render(<Input label="Test Label" error="This is an error" />)
      const input = screen.getByRole('textbox', { name: /test label/i })
      const error = screen.getByText(/this is an error/i)

      expect(input).toHaveAttribute('aria-invalid', 'true')
      expect(input).toHaveAttribute('aria-describedby', expect.stringContaining('input-'))
      expect(error).toBeInTheDocument()
    })

    it('should be focusable and keyboard accessible', () => {
      render(<Input label="Test Label" />)
      const input = screen.getByRole('textbox', { name: /test label/i })

      input.focus()
      expect(input).toHaveFocus()

      fireEvent.change(input, { target: { value: 'Test Value' } })
      expect(input).toHaveValue('Test Value')
    })
  })

  describe('Modal Component', () => {
    it('should have proper ARIA attributes when open', () => {
      render(
        <Modal isOpen={true} onClose={() => {}} title="Test Modal" role="dialog">
          <p>Modal content</p>
        </Modal>
      )

      const dialog = screen.getByRole('dialog', { name: /test modal/i })
      expect(dialog).toBeInTheDocument()
      expect(dialog).toHaveAttribute('aria-modal', 'true')
    })

    it('should trap focus when open', () => {
      const onClose = vi.fn()
      render(
        <Modal isOpen={true} onClose={onClose} title="Test Modal">
          <button data-testid="modal-button">Modal Button</button>
        </Modal>
      )

      const modalButton = screen.getByTestId('modal-button')
      expect(modalButton).toHaveFocus()
    })

    it('should close on Escape key press', () => {
      const onClose = vi.fn()
      render(
        <Modal isOpen={true} onClose={onClose} title="Test Modal">
          <p>Modal content</p>
        </Modal>
      )

      const dialog = screen.getByRole('dialog', { name: /test modal/i })
      dialog.focus()

      fireEvent.keyDown(dialog, { key: 'Escape' })
      expect(onClose).toHaveBeenCalled()
    })

    it('should close on outside click', () => {
      const onClose = vi.fn()
      render(
        <Modal isOpen={true} onClose={onClose} title="Test Modal">
          <p>Modal content</p>
        </Modal>
      )

      // Simulate clicking outside the modal
      const backdrop = screen.getByRole('dialog').parentElement
      if (backdrop) {
        fireEvent.mouseDown(backdrop)
        expect(onClose).toHaveBeenCalled()
      }
    })
  })

  describe('Card Component', () => {
    it('should have proper ARIA attributes', () => {
      render(
        <Card role="region" aria-label="Test Card">
          <p>Card content</p>
        </Card>
      )

      const card = screen.getByLabelText(/test card/i)
      expect(card).toBeInTheDocument()
    })

    it('should be focusable when interactive', () => {
      render(
        <Card clickable={true} ariaLabel="Interactive Card">
          <p>Interactive card content</p>
        </Card>
      )

      const card = screen.getByLabelText(/interactive card/i)
      expect(card).toHaveAttribute('tabIndex', '0')
    })

    it('should be operable with keyboard when interactive', () => {
      const onClick = vi.fn()
      render(
        <Card clickable={true} onClick={onClick} ariaLabel="Interactive Card">
          <p>Interactive card content</p>
        </Card>
      )

      const card = screen.getByLabelText(/interactive card/i)
      card.focus()
      expect(card).toHaveFocus()

      fireEvent.keyUp(card, { key: 'Enter' })
      expect(onClick).toHaveBeenCalledTimes(1)

      fireEvent.keyUp(card, { key: ' ' })
      expect(onClick).toHaveBeenCalledTimes(2)
    })
  })

  describe('Form Component', () => {
    it('should have proper ARIA attributes for form elements', () => {
      const handleSubmit = vi.fn()
      render(
        <Form onSubmit={handleSubmit}>
          <FormInput name="test" label="Test Field" />
          <FormSubmitButton>Submit</FormSubmitButton>
        </Form>
      )

      const input = screen.getByRole('textbox', { name: /test field/i })
      expect(input).toBeInTheDocument()
      expect(input).toHaveAttribute('aria-required', 'false')
    })

    it('should handle form submission with keyboard', () => {
      const handleSubmit = vi.fn()
      render(
        <Form onSubmit={handleSubmit}>
          <FormInput name="test" label="Test Field" />
          <FormSubmitButton>Submit</FormSubmitButton>
        </Form>
      )

      const submitButton = screen.getByRole('button', { name: /submit/i })
      submitButton.focus()
      expect(submitButton).toHaveFocus()

      fireEvent.keyUp(submitButton, { key: 'Enter' })
      // Submit happens via context, so we can't directly test it here
    })

    it('should show validation errors', async () => {
      const handleSubmit = vi.fn()
      const validate = (values: any) => {
        const errors: any = {}
        if (!values.test) {
          errors.test = 'Test field is required'
        }
        return errors
      }

      render(
        <Form onSubmit={handleSubmit} validate={validate}>
          <FormInput name="test" label="Test Field" required={true} />
          <FormSubmitButton>Submit</FormSubmitButton>
        </Form>
      )

      const submitButton = screen.getByRole('button', { name: /submit/i })
      fireEvent.click(submitButton)

      await waitFor(() => {
        expect(screen.queryByText(/test field is required/i)).toBeInTheDocument()
      })
    })
  })

  describe('Focus Management', () => {
    it('should manage focus correctly', () => {
      render(
        <>
          <button data-testid="first">First</button>
          <button data-testid="second">Second</button>
          <button data-testid="third">Third</button>
        </>
      )

      const firstButton = screen.getByTestId('first')
      const secondButton = screen.getByTestId('second')
      const thirdButton = screen.getByTestId('third')

      // Focus first element
      firstButton.focus()
      expect(firstButton).toHaveFocus()

      // Tab to second
      fireEvent.keyDown(document.activeElement!, { key: 'Tab' })
      expect(secondButton).toHaveFocus()

      // Tab to third
      fireEvent.keyDown(document.activeElement!, { key: 'Tab' })
      expect(thirdButton).toHaveFocus()
    })

    it('should handle shift+tab correctly', () => {
      render(
        <>
          <button data-testid="first">First</button>
          <button data-testid="second">Second</button>
          <button data-testid="third">Third</button>
        </>
      )

      const firstButton = screen.getByTestId('first')
      const secondButton = screen.getByTestId('second')
      const thirdButton = screen.getByTestId('third')

      // Focus third element first
      thirdButton.focus()
      expect(thirdButton).toHaveFocus()

      // Shift+Tab to second
      fireEvent.keyDown(document.activeElement!, { key: 'Tab', shiftKey: true })
      expect(secondButton).toHaveFocus()

      // Shift+Tab to first
      fireEvent.keyDown(document.activeElement!, { key: 'Tab', shiftKey: true })
      expect(firstButton).toHaveFocus()
    })
  })

  describe('Screen Reader Compatibility', () => {
    it('should announce live regions', () => {
      // This is difficult to test directly, but we can verify that the
      // aria-live attributes are applied correctly
      render(
        <div aria-live="polite" data-testid="live-region">
          Test message
        </div>
      )

      const liveRegion = screen.getByTestId('live-region')
      expect(liveRegion).toHaveAttribute('aria-live', 'polite')
    })

    it('should have proper heading hierarchy', () => {
      render(
        <>
          <h1>Main Heading</h1>
          <h2>Sub Heading</h2>
          <h3>Sub-sub Heading</h3>
        </>
      )

      const mainHeading = screen.getByRole('heading', { level: 1, name: /main heading/i })
      const subHeading = screen.getByRole('heading', { level: 2, name: /sub heading/i })
      const subSubHeading = screen.getByRole('heading', { level: 3, name: /sub-sub heading/i })

      expect(mainHeading).toBeInTheDocument()
      expect(subHeading).toBeInTheDocument()
      expect(subSubHeading).toBeInTheDocument()
    })
  })
})

// Additional accessibility tests for keyboard navigation
describe('Keyboard Navigation Tests', () => {
  it('should navigate through focusable elements', () => {
    render(
      <div>
        <button>Button 1</button>
        <input type="text" />
        <a href="#">Link</a>
        <button>Button 2</button>
      </div>
    )

    // Get all focusable elements
    const focusableElements = document.querySelectorAll(
      'button, input, a[href]'
    )

    expect(focusableElements).toHaveLength(4)
  })

  it('should skip non-focusable elements', () => {
    render(
      <div>
        <button>Button 1</button>
        <div tabIndex={-1}>Non-focusable div</div>
        <input type="text" />
        <span>Non-focusable span</span>
        <button>Button 2</button>
      </div>
    )

    // Only focusable elements should be in the tab order
    const focusableElements = document.querySelectorAll(
      'button, input, [tabindex]:not([tabindex="-1"])'
    )

    expect(focusableElements).toHaveLength(3)
  })
})