import React, { useState } from 'react';
import Button from './Button';
import InputGroup from './InputGroup';
import { ShieldCheck, Mail, Lock } from 'lucide-react';

export default function LoginPage({ onLoginSuccess }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError('Please fill in all fields');
      return;
    }
    setLoading(true);
    setError('');
    try {
      await onLoginSuccess(username, password);
    } catch (err) {
      setError(err.message || 'Login failed. Please check credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page-container animate-fade-in">
      <div className="login-card glass-panel accent-glow-border">
        <div className="login-header">
          <div className="login-logo">Σ</div>
          <h2>Sigma Statistics</h2>
          <p>Enterprise Workspace Portal Log In</p>
        </div>

        {error && (
          <div className="login-error-alert animate-fade-in">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="login-form">
          <InputGroup
            label="Username"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            placeholder="Enter username"
            icon={<Mail size={16} />}
          />

          <InputGroup
            label="Password"
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="Enter password"
            icon={<Lock size={16} />}
          />

          <div className="login-actions">
            <Button
              type="submit"
              variant="primary"
              disabled={loading}
              className="w-full"
            >
              {loading ? 'Authenticating…' : 'Secure Login'}
            </Button>
          </div>
        </form>

        <div className="login-footer">
          <ShieldCheck size={14} className="text-accent" />
          <span>Access restricted to verified enterprise personnel</span>
        </div>
      </div>
    </div>
  );
}
