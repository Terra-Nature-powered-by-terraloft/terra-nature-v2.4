import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import { axe, toHaveNoViolations } from 'jest-axe'
import { Dialog } from '../src/components/Dialog'

// Extend expect with jest-axe matchers
expect.extend(toHaveNoViolations)

describe('Dialog Accessibility', () => {
  it('should not have accessibility violations when open', async () => {
    const { container } = render(
      <Dialog isOpen={true} title="Test Dialog" onClose={() => {}}>
        <p>This is a test dialog content.</p>
        <button>Action Button</button>
      </Dialog>
    )

    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })

  it('should have proper ARIA attributes', () => {
    const { getByRole, getByLabelText } = render(
      <Dialog isOpen={true} title="Accessible Dialog" onClose={() => {}}>
        <p>Dialog content with proper accessibility.</p>
      </Dialog>
    )

    const dialog = getByRole('dialog')
    expect(dialog).toHaveAttribute('aria-modal', 'true')
    expect(dialog).toHaveAttribute('aria-labelledby', 'dialog-title')

    const closeButton = getByLabelText('Dialog schließen')
    expect(closeButton).toBeInTheDocument()

    const title = document.getElementById('dialog-title')
    expect(title).toHaveTextContent('Accessible Dialog')
  })

  it('should have proper focus management structure', () => {
    const { getByRole } = render(
      <Dialog isOpen={true} title="Focus Test" onClose={() => {}}>
        <input type="text" placeholder="First input" />
        <button>Action</button>
        <input type="text" placeholder="Last input" />
      </Dialog>
    )

    const dialog = getByRole('dialog')
    const document = getByRole('document')
    
    expect(dialog).toBeInTheDocument()
    expect(document).toBeInTheDocument()
    expect(document).toBeVisible()
  })

  it('should not render when closed (no accessibility concerns)', () => {
    const { container } = render(
      <Dialog isOpen={false} title="Closed Dialog" onClose={() => {}}>
        <p>This should not be rendered.</p>
      </Dialog>
    )

    expect(container.firstChild).toBeNull()
  })

  it('should have proper heading hierarchy', async () => {
    const { container } = render(
      <div>
        <h1>Main Page Title</h1>
        <Dialog isOpen={true} title="Dialog Title" onClose={() => {}}>
          <h3>Section in Dialog</h3>
          <p>Content under the section.</p>
        </Dialog>
      </div>
    )

    const results = await axe(container)
    expect(results).toHaveNoViolations()

    const dialogTitle = container.querySelector('#dialog-title')
    expect(dialogTitle?.tagName).toBe('H2')
  })

  it('should maintain color contrast standards', async () => {
    const { container } = render(
      <Dialog isOpen={true} title="Contrast Test" onClose={() => {}}>
        <p style={{ color: '#333', backgroundColor: '#fff' }}>
          This text should have sufficient contrast.
        </p>
        <button style={{ 
          backgroundColor: '#0d6efd', 
          color: '#fff',
          border: 'none',
          padding: '0.5rem 1rem' 
        }}>
          High Contrast Button
        </button>
      </Dialog>
    )

    const results = await axe(container)
    expect(results).toHaveNoViolations()
  })
})