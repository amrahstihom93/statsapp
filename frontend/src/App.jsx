import React, { useState, useEffect } from 'react';
import LayoutShell from './components/LayoutShell';
import Card from './components/Card';
import Button from './components/Button';
import OnboardingFlow from './components/OnboardingFlow';
import ClientManagement from './components/ClientManagement';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import DatasetManager from './components/DatasetManager';
import ProcessMapViewer from './components/ProcessMapViewer';
import StatsAnalyzer from './components/StatsAnalyzer';
import MLModelStudio from './components/MLModelStudio';
import FMEATracker from './components/FMEATracker';
import LoginPage from './components/LoginPage';
import { authAPI, clientsAPI, usersAPI } from './api/services';
import { 
  Users, 
  Building2, 
  Activity, 
  RefreshCw, 
  CheckCircle2, 
  Map, 
  Play, 
  ShieldCheck,
  TrendingUp,
  FileText
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [profile, setProfile] = useState(null);
  const [clients, setClients] = useState([]);
  const [users, setUsers] = useState([]);

  // Check auth status on load
  useEffect(() => {
    async function checkAuth() {
      try {
        const data = await authAPI.getMe();
        if (data.authenticated) {
          setProfile(data);
          setIsAuthenticated(true);
          // If admin, load clients and users list
          if (data.is_admin) {
            loadAdminData();
          }
        }
      } catch (err) {
        console.log("Not authenticated or server down:", err);
      } finally {
        setLoading(false);
      }
    }
    checkAuth();
  }, []);

  const loadAdminData = async () => {
    try {
      const [clientsList, usersList] = await Promise.all([
        clientsAPI.list(),
        usersAPI.list()
      ]);
      setClients(clientsList);
      setUsers(usersList);
    } catch (err) {
      console.error("Failed to load admin data:", err);
    }
  };

  const handleLogin = async (username, password) => {
    const data = await authAPI.login(username, password);
    setProfile(data);
    setIsAuthenticated(true);
    if (data.is_admin) {
      loadAdminData();
    }
  };

  // Callback to add a new client (triggered from ClientManagement form)
  const handleAddClient = async (newClient) => {
    const created = await clientsAPI.create(newClient.company_name, newClient.email_id);
    setClients(prev => [...prev, created]);
  };

  // Callback to map a user to a client (triggered from ClientManagement)
  const handleMapUser = async (userId, clientId) => {
    // Translate uuid back to django database pk if possible, or pass django_id
    const targetUser = users.find(u => u.user === userId || u.django_id === userId);
    if (!targetUser) return;
    const dbId = targetUser.django_id;
    await usersAPI.assignClient(dbId, clientId);
    
    // Refresh admin data to synchronize UI state
    await loadAdminData();

    // If current profile is mapped, update local state
    if (targetUser.username === profile.username) {
      const updatedMe = await authAPI.getMe();
      setProfile(updatedMe);
    }
  };

  // Callback when user onboarding flow is completed
  const handleOnboardingComplete = async (updatedProfile) => {
    await authAPI.completeTour();
    const fresh = await authAPI.getMe();
    setProfile(fresh);
    // Sync within users database list
    if (profile.is_admin) {
      loadAdminData();
    }
    setActiveTab('dashboard');
  };

  // Helper function to reset onboarding (for demonstration / verification purposes)
  const resetOnboarding = () => {
    const reset = {
      ...profile,
      phone_number: '',
      client: null,
      has_seen_tour: false
    };
    setProfile(reset);
    setActiveTab('onboarding');
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', height: '100vh', width: '100vw', alignItems: 'center', justifyContent: 'center', backgroundColor: '#050505', color: '#f4f4f5', fontFamily: 'monospace' }}>
        <span style={{ animation: 'pulseGlow 1.5s infinite', fontSize: '0.9rem', letterSpacing: '1px' }}>BOOTSTRAPPING PORTAL CONTEXT…</span>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <LoginPage onLoginSuccess={handleLogin} />;
  }

  return (
    <LayoutShell 
      activeTab={activeTab} 
      setActiveTab={setActiveTab} 
      profileData={profile}
    >
      {activeTab === 'dashboard' && (
        <div className="dashboard-overview animate-fade-in">
          
          {/* Welcome Dashboard Banner */}
          <div className="dashboard-hero-banner glass-panel">
            <div className="banner-left">
              <span className="banner-accent-tag">SYSTEM ONLINE</span>
              <h1 className="banner-heading">Sigma Workspaces</h1>
              <p className="banner-subtext">
                Deploy workflow metrics, manage organizational structures, and view analytical stats in real-time.
              </p>
            </div>
            <div className="banner-right">
              {profile.has_seen_tour ? (
                <div className="onboarding-completion-status text-accent">
                  <CheckCircle2 size={16} />
                  <span>Onboarding Checklist Complete</span>
                </div>
              ) : (
                <div className="onboarding-status-cta">
                  <span className="status-cta-text">Setup your workspace profile:</span>
                  <Button 
                    variant="primary" 
                    size="sm" 
                    onClick={() => setActiveTab('onboarding')}
                    icon={<Play size={12} />}
                  >
                    Start Tour
                  </Button>
                </div>
              )}
            </div>
          </div>

          {/* Quick Metrics Grid */}
          <div className="metrics-grid">
            <Card title="Organizations" subtitle="Linked Client IDs" glowOnHover={true}>
              <div className="metric-box">
                <Building2 className="metric-icon text-accent" size={32} />
                <div className="metric-content">
                  <span className="metric-value">{clients.length}</span>
                  <span className="metric-lbl">Active Clients</span>
                </div>
              </div>
            </Card>

            <Card title="Mapped Accounts" subtitle="Total profile databases" glowOnHover={true}>
              <div className="metric-box">
                <Users className="metric-icon text-accent" size={32} />
                <div className="metric-content">
                  <span className="metric-value">{users.length}</span>
                  <span className="metric-lbl">Active Users</span>
                </div>
              </div>
            </Card>

            <Card title="Process Maps" subtitle="Active tracing runs" glowOnHover={true}>
              <div className="metric-box">
                <Activity className="metric-icon text-accent" size={32} />
                <div className="metric-content">
                  <span className="metric-value">12 / Hour</span>
                  <span className="metric-lbl">Event Log Pipelines</span>
                </div>
              </div>
            </Card>
          </div>

          {/* Interactive Workspace Area */}
          <div className="dashboard-content-split">
            
            {/* Left: Dynamic Visualizer */}
            <div className="split-main">
              <Card title="Analytical Pipelines Graph" subtitle="Simulated Process Flow Mapping">
                <div className="visualizer-canvas-container glass-panel">
                  <div className="mock-flow-node start">
                    <div className="node-indicator active" />
                    <span className="node-lbl">Start</span>
                  </div>
                  
                  <div className="mock-flow-connector active">
                    <div className="connector-pulse" />
                  </div>
                  
                  <div className="mock-flow-node database-sync">
                    <DatabaseIcon className="node-icon" size={16} />
                    <span className="node-lbl">Read Data</span>
                  </div>

                  <div className="mock-flow-connector active">
                    <div className="connector-pulse" />
                  </div>

                  <div className="mock-flow-node processing-node">
                    <Activity size={16} className="node-icon animate-pulse-glow" />
                    <span className="node-lbl">Compute Regress</span>
                  </div>

                  <div className="mock-flow-connector">
                    <div className="connector-pulse" />
                  </div>

                  <div className="mock-flow-node end-node">
                    <div className="node-indicator" />
                    <span className="node-lbl">Output</span>
                  </div>
                </div>
                
                <div className="pipeline-details">
                  <div className="pipeline-stat-item">
                    <TrendingUp size={14} className="text-accent" />
                    <span>Average confidence score: <strong>98.5%</strong></span>
                  </div>
                  <div className="pipeline-stat-item">
                    <FileText size={14} className="text-secondary" />
                    <span>CSV event logs parsed: <strong>3,412 rows</strong></span>
                  </div>
                </div>
              </Card>
            </div>

            {/* Right: Operational Controls */}
            <div className="split-side">
              <Card title="System Diagnostics" subtitle="Admin and profile options">
                <div className="diagnostics-panel">
                  <div className="diagnostic-stat-row">
                    <span className="stat-lbl">Account Email:</span>
                    <span className="stat-val font-mono">{profile.email}</span>
                  </div>
                  <div className="diagnostic-stat-row">
                    <span className="stat-lbl">Client Domain:</span>
                    <span className="stat-val text-accent">
                      {profile.client ? profile.client.company_name : 'Unassigned'}
                    </span>
                  </div>
                  <div className="diagnostic-stat-row">
                    <span className="stat-lbl">Admin Status:</span>
                    <span className="stat-val text-success">
                      {profile.is_admin ? 'Superuser Verified' : 'Standard'}
                    </span>
                  </div>
                  <div className="diagnostic-stat-row">
                    <span className="stat-lbl">Onboarding Tour:</span>
                    <span className="stat-val">
                      {profile.has_seen_tour ? 'Completed' : 'Pending Setup'}
                    </span>
                  </div>

                  <div className="diagnostic-actions mt-4">
                    <Button 
                      variant="secondary" 
                      size="sm" 
                      onClick={resetOnboarding}
                      icon={<RefreshCw size={12} />}
                      className="w-full"
                    >
                      Reset Onboarding Flow
                    </Button>
                  </div>
                </div>
              </Card>
            </div>

          </div>

        </div>
      )}

      {activeTab === 'onboarding' && (
        <OnboardingFlow 
          profile={profile}
          onComplete={handleOnboardingComplete}
          availableClients={clients}
        />
      )}

      {activeTab === 'clients' && (
        <ClientManagement 
          clients={clients}
          users={users}
          onAddClient={handleAddClient}
          onMapUser={handleMapUser}
        />
      )}

      {activeTab === 'dashboard' && (
        <AnalyticsDashboard />
      )}

      {activeTab === 'datasets' && (
        <DatasetManager />
      )}

      {activeTab === 'stats' && (
        <StatsAnalyzer />
      )}

      {activeTab === 'mlstudio' && (
        <MLModelStudio />
      )}

      {activeTab === 'fmea' && (
        <FMEATracker />
      )}

      {activeTab === 'processmaps' && (
        <ProcessMapViewer />
      )}
    </LayoutShell>
  );
}

// Inline helper component for Database icon representation
function DatabaseIcon({ className, size }) {
  return (
    <svg 
      xmlns="http://www.w3.org/2000/svg" 
      viewBox="0 0 24 24" 
      fill="none" 
      stroke="currentColor" 
      strokeWidth="2" 
      strokeLinecap="round" 
      strokeLinejoin="round" 
      className={className}
      width={size}
      height={size}
    >
      <ellipse cx="12" cy="5" rx="9" ry="3" />
      <path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5" />
      <path d="M3 12c0 1.66 4 3 9 3s9-1.34 9-3" />
    </svg>
  );
}
