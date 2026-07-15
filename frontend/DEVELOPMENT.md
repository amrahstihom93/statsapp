# Sigma Statistics Frontend Development & Maintenance Guide

Welcome to the React workspace frontend documentation. This guide details the architecture, styling conventions, API integration layer, and maintenance routines for the dashboard.

---

## 1. Project Directory Structure

The frontend is a modern React application built on Vite.

```
frontend/
├── dist/                      # Compiled production assets
├── public/                    # Static public assets (icons, images)
├── src/
│   ├── api/                   # REST API Integration Layer
│   │   ├── client.js          # Base fetch client with session + CSRF forwarding
│   │   └── services.js        # Domain-specific API service wrappers
│   ├── components/            # Reusable UI Elements & View Tabs
│   │   ├── AnalyticsDashboard.jsx  # KPI tiles and real-time summaries
│   │   ├── Button.jsx         # Custom styled glassmorphic buttons
│   │   ├── Card.jsx           # Panel wrapper with glass backdrop & glows
│   │   ├── ClientManagement.jsx   # Admin organization & user mapping panel
│   │   ├── DatasetManager.jsx # Ingest, preview, and delete datasets
│   │   ├── FMEATracker.jsx    # Risk priority matrix & FMEA logging
│   │   ├── InputGroup.jsx     # Forms input text wrapper with validation states
│   │   ├── LoginPage.jsx      # Portal gateway access check screen
│   │   ├── MLModelStudio.jsx  # Regression fitting & PKL model training
│   │   ├── OnboardingFlow.jsx # Step-by-step interactive onboarding
│   │   └── ProcessMapViewer.jsx # Workspace process execution tracking
│   ├── App.jsx                # Main controller, state synchronization, and router
│   ├── index.css              # Cyberpunk variables, styles, and micro-animations
│   └── main.jsx               # Entry mounting point
├── DEVELOPMENT.md             # This document
├── index.html                 # HTML entry point (contains viewport & SEO tags)
├── package.json               # Package manifests and dependency controls
└── vite.config.js             # Vite compiler config
```

---

## 2. Architecture & State Design

### Gateway Authentication Flow
1. **On Mount**: `App.jsx` triggers `authAPI.getMe()` inside a `useEffect`.
2. **Bootstrapping**: Shows a dark loader until the session state is returned.
3. **Guard**: If the status is `401 Unauthenticated`, rendering falls back to the `LoginPage` component.
4. **Authorized Context**: Once the user logs in (`authAPI.login`), the user profile is cached in the local state, and the main `LayoutShell` mounts.

### Live Session Sharing (CORS & CSRF)
- Requests are handled by `src/api/client.js`.
- Always attaches `{ credentials: 'include' }` so the browser forwards the `sessionid` cookie on all API requests.
- Reads the CSRF token cookie via JavaScript (`getCookie('csrftoken')`) and appends it to the `X-CSRFToken` request header for POST, PUT, and DELETE queries.

---

## 3. Styling Guidelines (The Cyberpunk "Sigma" Theme)

The application utilizes an ultra-premium, dark-mode cyberpunk design theme.

### Color Tokens
Manage the following variables inside `index.css`:
- **Backgrounds**: `--bg-primary` (`#050505`) and `--bg-secondary` (`#0a0a0a`)
- **Accent Primary**: Electric Cyberpunk Cyan (`#00f0ff`) with matching glows
- **Accent Secondary**: Purple/Violet (`#a855f7`)

### Interactive Follow Cursor
The cursor follower is implemented in `LayoutShell.jsx` using simple mouse event listeners and a lerped rendering loop (`requestAnimationFrame`). Any hoverable or interactive element (like `button`, `input`, or `a`) will scale up the cursor and shift it to white with a cyan glow to indicate clickable feedback.

---

## 4. Maintenance Checklist for Frontend Updates

When adding a new tab or connecting new Django views:
1. **Declare the Endpoint**: Add the route function inside `src/api/services.js`.
2. **Manage CSRF**: If using POST, wrap parameters in `FormData` or configure raw JSON serialization.
3. **Register Tab**: Add an entry with a Lucide icon inside the `navItems` array of `LayoutShell.jsx`.
4. **Build Verification**: Run `npm run build` locally to confirm Vite compiles with zero errors before pushing upstream.