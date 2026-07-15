/**
 * Simple API helper for fetching from Django backend with session + CSRF tokens.
 */
const BASE_URL = 'http://localhost:8000';

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

export async function apiFetch(endpoint, options = {}) {
  // Ensure we have a CSRF cookie bootstrapped
  if (!getCookie('csrftoken') && endpoint !== '/api/v1/auth/csrf/') {
    try {
      await fetch(`${BASE_URL}/api/v1/auth/csrf/`, { credentials: 'include' });
    } catch (e) {
      console.warn('Failed to bootstrap CSRF cookie:', e);
    }
  }

  const url = endpoint.startsWith('http') ? endpoint : `${BASE_URL}${endpoint}`;
  
  // Set credentials default to include to pass sessions
  options.credentials = 'include';
  
  // Setup headers
  options.headers = options.headers || {};
  const csrfToken = getCookie('csrftoken');
  if (csrfToken) {
    options.headers['X-CSRFToken'] = csrfToken;
  }
  
  if (options.body && !(options.body instanceof FormData) && typeof options.body === 'object') {
    options.headers['Content-Type'] = 'application/json';
    options.body = JSON.stringify(options.body);
  }

  const response = await fetch(url, options);
  
  if (response.status === 401 && endpoint !== '/api/v1/auth/me/') {
    // Session expired or unauthenticated
    window.location.reload();
  }

  if (!response.ok) {
    let errData = {};
    try {
      errData = await response.json();
    } catch (_) {}
    throw new Error(errData.error || errData.message || `API error: ${response.status}`);
  }

  return response.json();
}
