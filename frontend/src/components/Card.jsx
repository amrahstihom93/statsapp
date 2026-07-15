import React from 'react';

/**
 * Flexible, glassmorphic Card container.
 * Props:
 * - title: string | ReactNode (heading)
 * - subtitle: string | ReactNode (secondary text below heading)
 * - headerExtra: ReactNode (aligned to the right side of header)
 * - footer: ReactNode (content at the bottom of the card)
 * - glowOnHover: boolean (glow neon border on hover)
 * - className: string
 * - children: ReactNode
 */
export default function Card({
  title,
  subtitle,
  headerExtra,
  footer,
  glowOnHover = true,
  className = '',
  children,
  ...props
}) {
  return (
    <div
      className={`glass-panel ${glowOnHover ? 'accent-glow-border' : ''} ${className}`}
      {...props}
    >
      {(title || subtitle || headerExtra) && (
        <div className="card-header">
          <div className="card-title-group">
            {title && <h3 className="card-title">{title}</h3>}
            {subtitle && <p className="card-subtitle">{subtitle}</p>}
          </div>
          {headerExtra && <div className="card-header-extra">{headerExtra}</div>}
        </div>
      )}
      
      <div className="card-body">
        {children}
      </div>
      
      {footer && (
        <div className="card-footer">
          {footer}
        </div>
      )}
    </div>
  );
}
