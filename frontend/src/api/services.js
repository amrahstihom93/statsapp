import { apiFetch } from './client';

export const authAPI = {
  getMe: () => apiFetch('/api/v1/auth/me/'),
  login: (username, password) => apiFetch('/api/v1/auth/login/', {
    method: 'POST',
    body: { username, password }
  }),
  logout: () => apiFetch('/api/v1/auth/logout/', { method: 'POST' }),
  completeTour: () => apiFetch('/api/v1/auth/complete-tour/', { method: 'POST' }),
};

export const clientsAPI = {
  list: () => apiFetch('/api/v1/clients/'),
  create: (company_name, email_id) => apiFetch('/api/v1/clients/', {
    method: 'POST',
    body: { company_name, email_id }
  }),
};

export const usersAPI = {
  list: () => apiFetch('/api/v1/users/'),
  assignClient: (userId, clientId) => apiFetch(`/api/v1/users/${userId}/assign-client/`, {
    method: 'POST',
    body: { client_id: clientId }
  }),
};

export const datasetsAPI = {
  list: () => apiFetch('/api/v1/datasets/'),
  upload: (datasetName, file, processId = '') => {
    const formData = new FormData();
    formData.append('datasetName', datasetName);
    formData.append('myfile', file);
    formData.append('process_id', processId);
    formData.append('fileType', file.name.split('.').pop() || 'csv');
    return apiFetch('/api/v1/datasets/upload/', {
      method: 'POST',
      body: formData,
    });
  },
  preview: (datasetId) => apiFetch(`/api/v1/datasets/${datasetId}/preview/`),
  delete: (datasetId) => apiFetch(`/api/v1/datasets/${datasetId}/`, { method: 'DELETE' }),
};

export const processesAPI = {
  list: () => apiFetch('/api/v1/processes/'),
  create: (process_name, parent_process = 'root') => apiFetch('/api/v1/processes/', {
    method: 'POST',
    body: { process_name, parent_process }
  }),
};

export const analyticsAPI = {
  listStats: () => apiFetch('/api/v1/analytics/stats/'),
  listMLModels: () => apiFetch('/api/v1/analytics/models/'),
  getSummary: () => apiFetch('/api/v1/analytics/summary/'),
  
  // Real statistical engine routes
  calculateStatistics: (datasetId, column, method = 'Descriptive Statistics') => {
    const fd = new FormData();
    fd.append('dataset_id', datasetId);
    fd.append('selecteddatacol', column);
    fd.append('selectedmethod', method);
    return apiFetch('/calculateStatistics/', { method: 'POST', body: fd });
  },
  saveStatistics: (name, datasetId, method, calculatedValue, fieldData) => {
    const fd = new FormData();
    fd.append('statistical_name', name);
    fd.append('dataset_id', datasetId);
    fd.append('selectedmethod', method);
    fd.append('statistical_calculated_value', JSON.stringify(calculatedValue));
    fd.append('fieldData', JSON.stringify(fieldData));
    return apiFetch('/saveStatistics/', { method: 'POST', body: fd });
  },
  
  // Real ML regression routes
  calculateRegression: (datasetId, dvar, idvar, trainingSize = 80, randomState = 42, fitIntercept = true) => {
    const fd = new FormData();
    fd.append('dataset_id', datasetId);
    fd.append('dvar', dvar);
    fd.append('idvar', idvar);
    fd.append('training_size', trainingSize);
    fd.append('random_state', randomState);
    fd.append('fit_intercept', fitIntercept ? 'True' : 'False');
    return apiFetch('/calcsregression/', { method: 'POST', body: fd });
  },
  saveMLModel: (modelName) => {
    const fd = new FormData();
    fd.append('model_name', modelName);
    return apiFetch('/saveMLmodel/', { method: 'POST', body: fd });
  },
  
  // Quality Tools (FMEA)
  listFMEA: () => apiFetch('/fmeaList/'),
  saveFMEA: (fmeaName, datasetId, calculatedValue, fieldData) => {
    const fd = new FormData();
    fd.append('fmea_name', fmeaName);
    fd.append('dataset_id', datasetId);
    fd.append('fmea_calculated_value', JSON.stringify(calculatedValue));
    fd.append('fieldData', JSON.stringify(fieldData));
    return apiFetch('/saveFMEA/', { method: 'POST', body: fd });
  }
};
