import React, { useState, useEffect } from 'react';
import { LayoutDashboard, UserCheck, Shield, Phone, Mail, CheckCircle2, XCircle, Users, Menu, X, BarChart2, Database, GitBranch, LogOut, Calculator, Cpu, ClipboardList } from 'lucide-react';
import { authAPI } from '../api/services';

/**
 * LayoutShell Component
 * Implements the main layout wrapper including sidebar, header, custom cursor, and responsive content view.
 */
export default function LayoutShell({
  activeTab,
  setActiveTab,
  profileData,
  children
}) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });
  const [outlinePos, setOutlinePos] = useState({ x: 0, y: 0 });
  const [isHoveringInteractive, setIsHoveringInteractive] = useState(false);

  // Mouse cursor follower logic
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePos({ x: e.clientX, y: e.clientY });
    };

    const handleMouseOver = (e) => {
      // Check if hovering over buttons, links, inputs or interactive elements
      const target = e.target;
      const isInteractive = 
        target.tagName === 'BUTTON' || 
        target.tagName === 'A' || 
        target.tagName === 'INPUT' || 
        target.closest('a') || 
        target.closest('button') ||
        target.classList.contains('pointer') ||
        target.style.cursor === 'pointer';
      
      setIsHoveringInteractive(!!isInteractive);
    };

    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseover', handleMouseOver);

    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseover', handleMouseOver);
    };
  }, []);

  // Smooth lerp animation for the cursor outline
  useEffect(() => {
    let animId;
    const updateOutline = () => {
      setOutlinePos((prev) => {
        const dx = mousePos.x - prev.x;
        const dy = mousePos.y - prev.y;
        // Lerp speed: 0.15 for smooth drag
        return {
          x: prev.x + dx * 0.15,
          y: prev.y + dy * 0.15
        };
      });
      animId = requestAnimationFrame(updateOutline);
    };
    animId = requestAnimationFrame(updateOutline);
    return () => cancelAnimationFrame(animId);
  }, [mousePos]);

  const navItems = [
    { id: 'dashboard',   label: 'Dashboard',          icon: LayoutDashboard },
    { id: 'datasets',    label: 'Datasets',           icon: Database        },
    { id: 'stats',       label: 'Stats Analyzer',     icon: Calculator      },
    { id: 'mlstudio',    label: 'ML Studio',          icon: Cpu             },
    { id: 'fmea',        label: 'FMEA Tools',         icon: ClipboardList   },
    { id: 'processmaps', label: 'Process Maps',       icon: GitBranch       },
    { id: 'onboarding',  label: 'Onboarding Flow',    icon: UserCheck       },
    { id: 'clients',     label: 'Client Management',  icon: Users           },
  ];

  return (
    <div className="layout-shell">
      {/* Custom follow cursors */}
      <div 
        className="custom-cursor-dot" 
        style={{ 
          left: `${mousePos.x}px`, 
          top: `${mousePos.y}px`,
          width: isHoveringInteractive ? '12px' : '8px',
          height: isHoveringInteractive ? '12px' : '8px',
          backgroundColor: isHoveringInteractive ? '#ffffff' : '#00f0ff'
        }} 
      />
      <div 
        className="custom-cursor-outline" 
        style={{ 
          left: `${outlinePos.x}px`, 
          top: `${outlinePos.y}px`,
          transform: `translate(-50%, -50%) scale(${isHoveringInteractive ? 1.5 : 1})`,
          borderColor: isHoveringInteractive ? '#00f0ff' : 'rgba(0, 240, 255, 0.4)',
          backgroundColor: isHoveringInteractive ? 'rgba(0, 240, 255, 0.05)' : 'transparent'
        }} 
      />

      {/* Sidebar navigation */}
      <aside className={`sidebar glass-panel ${sidebarOpen ? 'open' : 'collapsed'}`}>
        <div className="sidebar-brand">
          <div className="brand-logo">Σ</div>
          <span className="brand-text">SIGMA STATS</span>
        </div>

        <nav className="sidebar-nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`sidebar-link ${activeTab === item.id ? 'active' : ''}`}
              >
                <Icon size={18} />
                <span className="link-label">{item.label}</span>
                {activeTab === item.id && <div className="active-indicator" />}
              </button>
            );
          })}
        </nav>

        {/* User Profile Widget at the bottom */}
        {profileData && (
          <div className="sidebar-profile-widget">
            <div className="profile-header">
              <div className="profile-avatar">
                {profileData.email?.charAt(0).toUpperCase() || 'U'}
              </div>
              <div className="profile-info">
                <span className="profile-name">
                  {profileData.is_admin ? 'Admin Account' : 'Standard User'}
                </span>
                <span className="profile-client">
                  {profileData.client?.company_name || 'No Client Assigned'}
                </span>
              </div>
            </div>
            
            <div className="profile-details-list">
              <div className="profile-detail-item">
                <Mail size={12} className="text-secondary" />
                <span className="detail-value text-truncate">{profileData.email || 'N/A'}</span>
              </div>
              {profileData.phone_number && (
                <div className="profile-detail-item">
                  <Phone size={12} className="text-secondary" />
                  <span className="detail-value">{profileData.phone_number}</span>
                </div>
              )}
              <div className="profile-detail-item">
                {profileData.has_seen_tour ? (
                  <CheckCircle2 size={12} className="text-success" />
                ) : (
                  <XCircle size={12} className="text-error" />
                )}
                <span className="detail-value">
                  {profileData.has_seen_tour ? 'Tour Completed' : 'Tour Pending'}
                </span>
              </div>
            </div>

            <button
              onClick={async () => {
                try {
                  await authAPI.logout();
                  window.location.reload();
                } catch (e) {
                  console.error(e);
                }
              }}
              className="sidebar-link mt-3 text-error"
              style={{ borderTop: '1px solid var(--border-card)', paddingTop: '12px' }}
            >
              <LogOut size={14} />
              <span className="link-label">Log Out</span>
            </button>
          </div>
        )}
      </aside>

      {/* Main viewport */}
      <div className="main-viewport">
        {/* Top Header */}
        <header className="main-header glass-panel">
          <div className="header-left">
            <button 
              className="sidebar-toggle-btn"
              onClick={() => setSidebarOpen(!sidebarOpen)}
            >
              {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
            <h2 className="header-title">
              {navItems.find((n) => n.id === activeTab)?.label || 'Workspace'}
            </h2>
          </div>

          <div className="header-right">
            <div className="badge-system">
              {profileData?.is_admin && (
                <span className="admin-badge">
                  <Shield size={12} />
                  ADMINISTRATOR
                </span>
              )}
              <span className="status-badge">
                <span className="status-dot"></span>
                API CONNECTED
              </span>
            </div>
          </div>
        </header>

        {/* Content Container */}
        <main className="content-container animate-fade-in">
          {children}
        </main>
      </div>
    </div>
  );
}
