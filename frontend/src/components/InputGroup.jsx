import React from 'react';

/**
 * Premium, glass-styled InputGroup component with validation states.
 * Props:
 * - label: string (input label)
 * - name: string (input name attribute)
 * - type: string (default: 'text')
 * - value: string | number
 * - onChange: function
 * - placeholder: string
 * - error: string (displays error message and colors border red)
 * - success: boolean | string (colors border green or displays success message)
 * - icon: ReactNode (optional icon rendered inside the input box)
 * - required: boolean
 * - className: string
 */
export default function InputGroup({
  label,
  name,
  type = 'text',
  value,
  onChange,
  placeholder,
  error,
  success,
  icon,
  required = false,
  className = '',
  ...props
}) {
  const hasError = !!error;
  const hasSuccess = !!success;
  
  let inputStateClass = '';
  if (hasError) inputStateClass = 'input-error';
  else if (hasSuccess) inputStateClass = 'input-success';

  return (
    <div className={`input-group-container ${className}`}>
      {label && (
        <label htmlFor={name} className="input-label">
          {label} {required && <span className="label-required">*</span>}
        </label>
      )}
      
      <div className="input-wrapper">
        {icon && <span className="input-icon-left">{icon}</span>}
        <input
          id={name}
          name={name}
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          className={`input-field ${icon ? 'input-with-icon' : ''} ${inputStateClass}`}
          {...props}
        />
      </div>
      
      {hasError && <p className="input-feedback-error">{error}</p>}
      {hasSuccess && typeof success === 'string' && (
        <p className="input-feedback-success">{success}</p>
      )}
    </div>
  );
}
