import React from 'react';

/**
 * Premium glass/neon Button component following the Sigma design system.
 * Props:
 * - variant: 'primary' | 'secondary' (default: 'primary')
 * - size: 'sm' | 'md' | 'lg' (default: 'md')
 * - disabled: boolean
 * - onClick: function
 * - icon: ReactNode (optional icon)
 * - children: ReactNode
 */
export default function Button({
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  icon,
  children,
  className = '',
  ...props
}) {
  const baseClass = 'btn';
  const variantClass = `btn-${variant}`;
  const sizeClass = `btn-${size}`;
  
  return (
    <button
      className={`${baseClass} ${variantClass} ${sizeClass} ${disabled ? 'btn-disabled' : ''} ${className}`}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {icon && <span className="btn-icon">{icon}</span>}
      <span className="btn-content">{children}</span>
    </button>
  );
}
