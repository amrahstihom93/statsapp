import React, { useState } from 'react';
import Card from './Card';
import Button from './Button';
import InputGroup from './InputGroup';
import { 
  Compass, 
  Smartphone, 
  Building2, 
  ArrowRight, 
  ArrowLeft, 
  Sparkles, 
  Database, 
  GitFork, 
  BarChart3, 
  CheckCircle2, 
  Info,
  Mail 
} from 'lucide-react';

// Define state machine states
const STATES = {
  WELCOME: 'WELCOME',
  PROFILE_SETUP: 'PROFILE_SETUP',
  CLIENT_ASSIGNMENT: 'CLIENT_ASSIGNMENT',
  FEATURE_TOUR: 'FEATURE_TOUR',
  COMPLETE: 'COMPLETE'
};

const STEPS_ORDER = [
  STATES.WELCOME,
  STATES.PROFILE_SETUP,
  STATES.CLIENT_ASSIGNMENT,
  STATES.FEATURE_TOUR,
  STATES.COMPLETE
];

export default function OnboardingFlow({ 
  profile, 
  onComplete, 
  availableClients = [] 
}) {
  const [currentState, setCurrentState] = useState(STATES.WELCOME);
  
  // Form states
  const [phoneNumber, setPhoneNumber] = useState(profile.phone_number || '');
  const [phoneError, setPhoneError] = useState('');
  
  const [clientMode, setClientMode] = useState('select'); // 'select' | 'create'
  const [selectedClientId, setSelectedClientId] = useState(profile.client?.client_id || '');
  const [newClientName, setNewClientName] = useState('');
  const [newClientEmail, setNewClientEmail] = useState('');
  const [clientError, setClientError] = useState('');

  // Tour state
  const [tourIndex, setTourIndex] = useState(0);

  const tourSlides = [
    {
      title: "Interactive Workspace Datasets",
      description: "Manage, filter, and preprocess raw client statistics. Build custom clean tabular datasets directly within the glassmorphic cloud portal.",
      icon: Database,
      highlight: "Real-time updates & formatting"
    },
    {
      title: "Process Mining & Maps",
      description: "Automatically reconstruct your business process maps. Discover operational bottlenecks, loops, and deviances using our advanced node-link graphs.",
      icon: GitFork,
      highlight: "Dynamic route rendering"
    },
    {
      title: "Advanced Statistics & Analytics",
      description: "Inject AI models to forecast trends, estimate regression scores, and run hypothesis tests with high precision.",
      icon: BarChart3,
      highlight: "Awwwards-winning neon visualizations"
    }
  ];

  // State transitions (State Machine logic)
  const transitionTo = (nextState) => {
    setCurrentState(nextState);
  };

  const handleNext = () => {
    switch (currentState) {
      case STATES.WELCOME:
        transitionTo(STATES.PROFILE_SETUP);
        break;
        
      case STATES.PROFILE_SETUP:
        // Validate phone number
        if (!phoneNumber) {
          setPhoneError('Phone number is required to receive security updates.');
          return;
        }
        const phoneRegex = /^\+?[1-9]\d{1,14}$/;
        if (!phoneRegex.test(phoneNumber.replace(/\s+/g, ''))) {
          setPhoneError('Please enter a valid international phone number (e.g. +1 555 123 4567).');
          return;
        }
        setPhoneError('');
        transitionTo(STATES.CLIENT_ASSIGNMENT);
        break;
        
      case STATES.CLIENT_ASSIGNMENT:
        if (clientMode === 'select') {
          if (!selectedClientId) {
            setClientError('Please select a client organization.');
            return;
          }
        } else {
          if (!newClientName) {
            setClientError('Company name is required.');
            return;
          }
          if (!newClientEmail || !newClientEmail.includes('@')) {
            setClientError('Please enter a valid company email.');
            return;
          }
        }
        setClientError('');
        transitionTo(STATES.FEATURE_TOUR);
        break;
        
      case STATES.FEATURE_TOUR:
        if (tourIndex < tourSlides.length - 1) {
          setTourIndex(tourIndex + 1);
        } else {
          transitionTo(STATES.COMPLETE);
        }
        break;
        
      default:
        break;
    }
  };

  const handleBack = () => {
    switch (currentState) {
      case STATES.PROFILE_SETUP:
        transitionTo(STATES.WELCOME);
        break;
      case STATES.CLIENT_ASSIGNMENT:
        transitionTo(STATES.PROFILE_SETUP);
        break;
      case STATES.FEATURE_TOUR:
        if (tourIndex > 0) {
          setTourIndex(tourIndex - 1);
        } else {
          transitionTo(STATES.CLIENT_ASSIGNMENT);
        }
        break;
      case STATES.COMPLETE:
        transitionTo(STATES.FEATURE_TOUR);
        break;
      default:
        break;
    }
  };

  const handleFinish = () => {
    let finalClient = null;
    
    if (clientMode === 'select') {
      finalClient = availableClients.find(c => c.client_id === selectedClientId) || null;
    } else {
      finalClient = {
        client_id: `cli_${Math.random().toString(36).substr(2, 9)}`,
        company_name: newClientName,
        email_id: newClientEmail
      };
    }

    const updatedProfile = {
      ...profile,
      phone_number: phoneNumber,
      client: finalClient,
      has_seen_tour: true
    };
    
    onComplete(updatedProfile);
  };

  // Helper to render current state content
  const renderContent = () => {
    switch (currentState) {
      case STATES.WELCOME:
        return (
          <div className="onboarding-welcome animate-fade-in">
            <div className="onboarding-icon-main">
              <Sparkles size={48} className="text-accent" />
            </div>
            <h1 className="onboarding-title text-center">Welcome to Sigma</h1>
            <p className="onboarding-intro text-center">
              Let's complete your profile configuration and discover your new analytics workspace in just a few quick steps.
            </p>
            <div className="onboarding-features-list">
              <div className="onboarding-bullet">
                <CheckCircle2 size={16} className="text-accent" />
                <span>Verify user credentials and profiles</span>
              </div>
              <div className="onboarding-bullet">
                <CheckCircle2 size={16} className="text-accent" />
                <span>Link workspace to a client list</span>
              </div>
              <div className="onboarding-bullet">
                <CheckCircle2 size={16} className="text-accent" />
                <span>Explore dynamic data visualization panels</span>
              </div>
            </div>
          </div>
        );

      case STATES.PROFILE_SETUP:
        return (
          <div className="onboarding-profile animate-fade-in">
            <h2 className="onboarding-section-title">Configure Profile</h2>
            <p className="onboarding-section-desc">
              Please enter your contact details. This links your account to organizational safety configurations.
            </p>
            <div className="onboarding-form-group">
              <InputGroup
                label="Registered Email"
                name="email"
                value={profile.email}
                disabled={true}
                placeholder="email@example.com"
                icon={<Mail size={16} />}
              />
              <InputGroup
                label="Phone Number"
                name="phone"
                value={phoneNumber}
                onChange={(e) => {
                  setPhoneNumber(e.target.value);
                  if (phoneError) setPhoneError('');
                }}
                required={true}
                placeholder="+1 555 123 4567"
                error={phoneError}
                icon={<Smartphone size={16} />}
              />
            </div>
          </div>
        );

      case STATES.CLIENT_ASSIGNMENT:
        return (
          <div className="onboarding-client animate-fade-in">
            <h2 className="onboarding-section-title">Client Assignment</h2>
            <p className="onboarding-section-desc">
              Associate this account with an organization to unlock relevant statistics datasets.
            </p>
            
            <div className="client-tabs">
              <button 
                className={`client-tab-btn ${clientMode === 'select' ? 'active' : ''}`}
                onClick={() => {
                  setClientMode('select');
                  setClientError('');
                }}
              >
                Choose Existing
              </button>
              <button 
                className={`client-tab-btn ${clientMode === 'create' ? 'active' : ''}`}
                onClick={() => {
                  setClientMode('create');
                  setClientError('');
                }}
              >
                Register New
              </button>
            </div>

            {clientError && (
              <div className="client-error-banner">
                <Info size={14} />
                <span>{clientError}</span>
              </div>
            )}

            {clientMode === 'select' ? (
              <div className="client-selector-box">
                {availableClients.length === 0 ? (
                  <p className="text-muted text-center py-4">No client records found. Please register a new client.</p>
                ) : (
                  <div className="client-grid">
                    {availableClients.map((c) => (
                      <div 
                        key={c.client_id}
                        className={`client-card glass-panel ${selectedClientId === c.client_id ? 'selected' : ''}`}
                        onClick={() => {
                          setSelectedClientId(c.client_id);
                          setClientError('');
                        }}
                      >
                        <Building2 size={24} className={selectedClientId === c.client_id ? 'text-accent' : 'text-secondary'} />
                        <div className="client-card-info">
                          <h4 className="client-card-title">{c.company_name}</h4>
                          <span className="client-card-id">{c.client_id}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <div className="client-create-box">
                <InputGroup
                  label="Company Name"
                  name="companyName"
                  value={newClientName}
                  onChange={(e) => {
                    setNewClientName(e.target.value);
                    if (clientError) setClientError('');
                  }}
                  required={true}
                  placeholder="Sigma Solutions Inc."
                  icon={<Building2 size={16} />}
                />
                <InputGroup
                  label="Corporate Billing Email"
                  name="companyEmail"
                  value={newClientEmail}
                  onChange={(e) => {
                    setNewClientEmail(e.target.value);
                    if (clientError) setClientError('');
                  }}
                  required={true}
                  placeholder="billing@sigmasolutions.com"
                  icon={<Mail size={16} />}
                />
              </div>
            )}
          </div>
        );

      case STATES.FEATURE_TOUR:
        const slide = tourSlides[tourIndex];
        const SlideIcon = slide.icon;
        return (
          <div className="onboarding-tour animate-fade-in">
            <div className="tour-badge">
              <Compass size={12} />
              <span>EXPLORING SYSTEM</span>
            </div>
            
            <div className="tour-slide-container">
              <div className="tour-slide-art">
                <div className="tour-art-icon-ring">
                  <SlideIcon size={40} className="text-accent" />
                </div>
                <div className="tour-highlight-tag">{slide.highlight}</div>
              </div>
              
              <div className="tour-slide-text">
                <h2 className="tour-slide-title">{slide.title}</h2>
                <p className="tour-slide-desc">{slide.description}</p>
              </div>
            </div>

            <div className="tour-dots">
              {tourSlides.map((_, i) => (
                <div 
                  key={i} 
                  className={`tour-dot ${i === tourIndex ? 'active' : ''}`}
                  onClick={() => setTourIndex(i)}
                />
              ))}
            </div>
          </div>
        );

      case STATES.COMPLETE:
        return (
          <div className="onboarding-complete animate-fade-in">
            <div className="complete-checkmark-wrapper">
              <CheckCircle2 size={56} className="text-accent animate-pulse-glow" />
            </div>
            <h1 className="onboarding-title text-center">Setup Complete</h1>
            <p className="onboarding-intro text-center">
              Your profile is verified and linked. You're ready to access the Sigma statistics interactive interface.
            </p>

            <div className="summary-card glass-panel">
              <div className="summary-row">
                <span className="summary-lbl">Phone Number:</span>
                <span className="summary-val">{phoneNumber}</span>
              </div>
              <div className="summary-row">
                <span className="summary-lbl">Linked Client:</span>
                <span className="summary-val">
                  {clientMode === 'select' 
                    ? availableClients.find(c => c.client_id === selectedClientId)?.company_name 
                    : newClientName}
                </span>
              </div>
              <div className="summary-row">
                <span className="summary-lbl">Onboarding Tour:</span>
                <span className="summary-val text-accent">COMPLETED</span>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  const stepIndex = STEPS_ORDER.indexOf(currentState);
  const totalSteps = STEPS_ORDER.length;
  const progressPercent = ((stepIndex + 1) / totalSteps) * 100;

  return (
    <div className="onboarding-flow-container">
      {/* Onboarding steps header */}
      <div className="onboarding-header">
        <div className="onboarding-progress-track">
          <div className="onboarding-progress-bar" style={{ width: `${progressPercent}%` }} />
        </div>
        <div className="onboarding-steps-indicator">
          {STEPS_ORDER.map((state, idx) => (
            <div 
              key={state}
              className={`step-indicator-node 
                ${idx < stepIndex ? 'completed' : ''} 
                ${idx === stepIndex ? 'active' : ''}
              `}
            >
              <div className="node-dot">
                {idx < stepIndex ? '✓' : idx + 1}
              </div>
              <span className="node-label">
                {state.replace('_', ' ')}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* Main card */}
      <Card className="onboarding-card">
        <div className="onboarding-card-content">
          {renderContent()}
        </div>

        <div className="onboarding-card-footer">
          {currentState !== STATES.WELCOME && (
            <Button 
              variant="secondary" 
              size="md" 
              onClick={handleBack}
              icon={<ArrowLeft size={16} />}
            >
              Back
            </Button>
          )}
          
          {currentState === STATES.COMPLETE ? (
            <Button 
              variant="primary" 
              size="md" 
              onClick={handleFinish}
              className="ml-auto"
            >
              Finish Setup
            </Button>
          ) : (
            <Button 
              variant="primary" 
              size="md" 
              onClick={handleNext}
              className="ml-auto"
              icon={<ArrowRight size={16} />}
            >
              {currentState === STATES.WELCOME ? 'Get Started' : 'Next Step'}
            </Button>
          )}
        </div>
      </Card>
    </div>
  );
}
