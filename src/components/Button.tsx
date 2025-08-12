import React from 'react'

export interface ButtonProps {
  /**
   * Is this the principal call to action on the page?
   */
  primary?: boolean
  /**
   * What background color to use
   */
  variant?: 'primary' | 'secondary' | 'danger'
  /**
   * How large should the button be?
   */
  size?: 'small' | 'medium' | 'large'
  /**
   * Button contents
   */
  children: React.ReactNode
  /**
   * Optional click handler
   */
  onClick?: () => void
  /**
   * Is the button disabled?
   */
  disabled?: boolean
  /**
   * Additional CSS classes
   */
  className?: string
  /**
   * Button type
   */
  type?: 'button' | 'submit' | 'reset'
}

/**
 * Primary UI component for user interaction
 */
export const Button = ({
  primary = false,
  variant = 'primary',
  size = 'medium',
  children,
  className = '',
  disabled = false,
  type = 'button',
  ...props
}: ButtonProps) => {
  const variantClass = primary ? 'btn-primary' : `btn-${variant}`
  const sizeClass = size !== 'medium' ? `btn-${size}` : ''
  
  return (
    <button
      type={type}
      className={`btn ${variantClass} ${sizeClass} ${className}`.trim()}
      disabled={disabled}
      {...props}
    >
      {children}
    </button>
  )
}

export default Button