import React from 'react'

export interface DialogProps {
  /**
   * Is the dialog open?
   */
  isOpen: boolean
  /**
   * Dialog title
   */
  title: string
  /**
   * Dialog content
   */
  children: React.ReactNode
  /**
   * Function to call when dialog should be closed
   */
  onClose: () => void
  /**
   * Additional CSS classes
   */
  className?: string
}

/**
 * Modal dialog component with accessibility features
 */
export const Dialog = ({
  isOpen,
  title,
  children,
  onClose,
  className = '',
}: DialogProps) => {
  if (!isOpen) return null

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose()
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      onClose()
    }
  }

  return (
    <div
      className={`dialog-backdrop ${className}`}
      onClick={handleBackdropClick}
      onKeyDown={handleKeyDown}
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="dialog-title"
    >
      <div
        style={{
          backgroundColor: 'white',
          padding: '2rem',
          borderRadius: '0.5rem',
          maxWidth: '500px',
          width: '90%',
          maxHeight: '80vh',
          overflow: 'auto',
        }}
        role="document"
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '1rem',
          }}
        >
          <h2 id="dialog-title" style={{ margin: 0 }}>
            {title}
          </h2>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '1.5rem',
              cursor: 'pointer',
              padding: '0.25rem',
            }}
            aria-label="Dialog schließen"
          >
            ×
          </button>
        </div>
        <div>{children}</div>
      </div>
    </div>
  )
}

export default Dialog