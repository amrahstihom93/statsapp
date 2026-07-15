import React, { useState } from 'react';
import Card from './Card';
import Button from './Button';
import InputGroup from './InputGroup';
import { 
  Building2, 
  Search, 
  Plus, 
  UserPlus, 
  Mail, 
  Trash2, 
  Check, 
  AlertTriangle 
} from 'lucide-react';

export default function ClientManagement({ 
  clients = [], 
  users = [], 
  onAddClient, 
  onMapUser 
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [showAddForm, setShowAddForm] = useState(false);
  
  // New Client Form State
  const [clientId, setClientId] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [emailId, setEmailId] = useState('');
  const [formErrors, setFormErrors] = useState({});

  // Map User Form State
  const [selectedUserId, setSelectedUserId] = useState('');
  const [selectedClientId, setSelectedClientId] = useState('');
  const [mapSuccess, setMapSuccess] = useState('');
  const [mapError, setMapError] = useState('');

  // Handle Search Filtering
  const filteredClients = clients.filter(client => 
    client.company_name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    client.client_id.toLowerCase().includes(searchQuery.toLowerCase())
  );

  // Validate and submit new client registration
  const handleCreateClient = (e) => {
    e.preventDefault();
    const errors = {};
    
    if (!clientId) {
      errors.clientId = 'Client ID is required.';
    } else if (!/^[a-zA-Z0-9_-]{3,15}$/.test(clientId)) {
      errors.clientId = 'Client ID must be 3-15 alphanumeric characters (dashes/underscores allowed).';
    } else if (clients.some(c => c.client_id === clientId)) {
      errors.clientId = 'This Client ID is already registered.';
    }

    if (!companyName) {
      errors.companyName = 'Company name is required.';
    } else if (companyName.length < 3) {
      errors.companyName = 'Company name must be at least 3 characters.';
    }

    if (!emailId) {
      errors.emailId = 'Contact email is required.';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailId)) {
      errors.emailId = 'Please enter a valid email address.';
    }

    if (Object.keys(errors).length > 0) {
      setFormErrors(errors);
      return;
    }

    setFormErrors({});
    
    // Trigger parent callback
    onAddClient({
      client_id: clientId,
      company_name: companyName,
      email_id: emailId
    });

    // Reset Form
    setClientId('');
    setCompanyName('');
    setEmailId('');
    setShowAddForm(false);
  };

  // Handle User Mapping Submission
  const handleMapUserSubmit = (e) => {
    e.preventDefault();
    if (!selectedUserId) {
      setMapError('Please select a user account.');
      return;
    }
    if (!selectedClientId) {
      setMapError('Please select a target client organization.');
      return;
    }

    setMapError('');
    onMapUser(selectedUserId, selectedClientId);
    
    const uName = users.find(u => u.user === selectedUserId)?.email || 'User';
    const cName = clients.find(c => c.client_id === selectedClientId)?.company_name || 'Client';
    
    setMapSuccess(`Successfully mapped account ${uName} to ${cName}`);
    setSelectedUserId('');
    setSelectedClientId('');
    
    setTimeout(() => {
      setMapSuccess('');
    }, 4000);
  };

  return (
    <div className="client-management-workspace animate-fade-in">
      <div className="workspace-grid">
        
        {/* Left Column: Client List & Controls */}
        <div className="workspace-main-column">
          <Card 
            title="Registered Client Organizations"
            subtitle="View, search, and manage your linked enterprise accounts"
            headerExtra={
              <Button 
                variant={showAddForm ? "secondary" : "primary"}
                size="sm"
                onClick={() => setShowAddForm(!showAddForm)}
                icon={<Plus size={14} />}
              >
                {showAddForm ? 'Close panel' : 'Add Client'}
              </Button>
            }
          >
            {/* Search Input bar */}
            <div className="search-bar-container">
              <Search size={16} className="search-icon" />
              <input 
                type="text" 
                placeholder="Search clients by ID or company name..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-input"
              />
            </div>

            {/* In-place registration Form */}
            {showAddForm && (
              <form onSubmit={handleCreateClient} className="add-client-form glass-panel animate-fade-in">
                <h4 className="form-heading-internal">Register New Client</h4>
                
                <div className="form-grid-2col">
                  <InputGroup
                    label="Client ID (Unique Key)"
                    name="newClientId"
                    value={clientId}
                    onChange={(e) => {
                      setClientId(e.target.value);
                      if (formErrors.clientId) setFormErrors({...formErrors, clientId: ''});
                    }}
                    required={true}
                    placeholder="e.g. delta-corp"
                    error={formErrors.clientId}
                  />
                  <InputGroup
                    label="Company Name"
                    name="newCompanyName"
                    value={companyName}
                    onChange={(e) => {
                      setCompanyName(e.target.value);
                      if (formErrors.companyName) setFormErrors({...formErrors, companyName: ''});
                    }}
                    required={true}
                    placeholder="e.g. Delta Systems LLC"
                    error={formErrors.companyName}
                  />
                </div>

                <InputGroup
                  label="Primary Contact Email"
                  name="newEmailId"
                  value={emailId}
                  onChange={(e) => {
                    setEmailId(e.target.value);
                    if (formErrors.emailId) setFormErrors({...formErrors, emailId: ''});
                  }}
                  required={true}
                  placeholder="e.g. admin@deltasystems.com"
                  error={formErrors.emailId}
                  icon={<Mail size={16} />}
                />

                <div className="form-actions">
                  <Button 
                    type="submit" 
                    variant="primary" 
                    size="sm"
                  >
                    Confirm Registration
                  </Button>
                </div>
              </form>
            )}

            {/* Clients Listing */}
            <div className="clients-list-container">
              {filteredClients.length === 0 ? (
                <div className="empty-state">
                  <Building2 size={36} className="text-secondary" />
                  <p className="text-muted">No client records match your query.</p>
                </div>
              ) : (
                <div className="clients-table-wrapper">
                  <table className="clients-table">
                    <thead>
                      <tr>
                        <th>Client ID</th>
                        <th>Company Name</th>
                        <th>Contact Email</th>
                        <th>Mapped Users</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredClients.map((client) => {
                        const mappedCount = users.filter(u => u.client?.client_id === client.client_id).length;
                        return (
                          <tr key={client.client_id} className="client-table-row">
                            <td className="client-id-cell font-mono">{client.client_id}</td>
                            <td className="client-name-cell">{client.company_name}</td>
                            <td className="client-email-cell">{client.email_id}</td>
                            <td>
                              <span className="mapped-badge">
                                {mappedCount} {mappedCount === 1 ? 'user' : 'users'}
                              </span>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </Card>
        </div>

        {/* Right Column: User Mapping & Operations */}
        <div className="workspace-sidebar-column">
          <Card 
            title="User Account Mapping" 
            subtitle="Link individual user profiles to client organizations"
          >
            <form onSubmit={handleMapUserSubmit} className="map-user-form">
              {mapSuccess && (
                <div className="map-alert success animate-fade-in">
                  <Check size={14} />
                  <span>{mapSuccess}</span>
                </div>
              )}

              {mapError && (
                <div className="map-alert error animate-fade-in">
                  <AlertTriangle size={14} />
                  <span>{mapError}</span>
                </div>
              )}

              <div className="form-select-group">
                <label className="input-label">Select User Account</label>
                <div className="select-wrapper">
                  <select 
                    value={selectedUserId} 
                    onChange={(e) => setSelectedUserId(e.target.value)}
                    className="select-field"
                  >
                    <option value="">-- Choose User Profile --</option>
                    {users.map((u) => (
                      <option key={u.user} value={u.user}>
                        {u.email} ({u.client?.company_name || 'No Client'})
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="form-select-group">
                <label className="input-label">Target Organization</label>
                <div className="select-wrapper">
                  <select 
                    value={selectedClientId} 
                    onChange={(e) => setSelectedClientId(e.target.value)}
                    className="select-field"
                  >
                    <option value="">-- Select Client Organization --</option>
                    {clients.map((c) => (
                      <option key={c.client_id} value={c.client_id}>
                        {c.company_name} ({c.client_id})
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <Button 
                type="submit" 
                variant="primary" 
                size="md" 
                className="w-full mt-4"
                icon={<UserPlus size={16} />}
              >
                Map Account
              </Button>
            </form>
          </Card>
        </div>

      </div>
    </div>
  );
}
