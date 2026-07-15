# Sigma Statistics (StatsApp)

## Overview
A hybrid Django + AngularJS/React statistics/data platform, imported from GitHub. Users upload datasets and run visualizations, statistical tests, ML models, process maps, and quality tools (FMEA) against them.

## Architecture
- **Backend**: Django 4.2 + Django REST Framework. Apps live under `apps/` (`accounts`, `datasets`, `analytics`, `processes`, `machinelearning`, `processmap`, `qualitytools`) plus `core/` for landing/auth pages. Settings are split under `config/settings/` (`base.py` + `local.py`); `manage.py` defaults to `config.settings.local`.
- **Legacy frontend**: Server-rendered Django templates + AngularJS (1.2.5) SPA routing for the dataset workspace (`apps/datasets/templates/datasets/datasetlist.html`, `static/js/app.js`). Some legacy static assets referenced here (`angular1.2.5.js`, `jquery-3.2.1.min.js`, `bootstrap.min.js`) are missing from `static/` and 404 — pre-existing from the import, not caused by this setup.
- **New frontend**: `frontend/` is a separate Vite + React 19 app (not yet wired into the Django app) with a fairly complete component set already (`LayoutShell`, `Card`, `Button`, `OnboardingFlow`, `ClientManagement`, `AnalyticsDashboard`, `DatasetManager`, `ProcessMapViewer`, `StatsAnalyzer`, `MLModelStudio`, `FMEATracker`, `LoginPage`) that talks to the `api/v1/...` JSON endpoints. It builds cleanly (`npm run build`) but isn't served by anything yet.
- **Database**: SQLite (`db.sqlite3`), already populated from the import. Swappable to Postgres via `DB_ENGINE` env var (see `.env.example`).

## Running it
- The `Django Server` workflow runs `python3 manage.py runserver 0.0.0.0:5000` — this is what the Replit preview shows.
- Config (`SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`, DB/email settings) is provided via Replit environment variables (shared), not a `.env` file — `python-decouple` reads them directly from the environment.
- `CSRF_TRUSTED_ORIGINS` in `config/settings/base.py` was extended to trust the Replit dev domain(s) so login/admin POSTs work through the webview proxy.
- To work on the new React frontend: `cd frontend && npm run dev` (Vite, not wired to a workflow yet since it isn't connected to the app).

## Setup notes / fixes made while importing
- `requirements.txt` pinned `Django==4.2.13`, which is blocked by Replit's package security firewall (known CVE-affected release); bumped to `Django==4.2.30` (same 4.2 line, latest patch).
- `config/urls.py` had a large block of routes referencing view modules (`core_views`, `accounts_views`, `chart_views`, `accounts_api`, etc.) that were never imported — Django couldn't even boot. Every one of those routes was already duplicated via the `include()` calls further down (each app's own `urls.py`/`api_urls.py`), so the broken duplicate block and a duplicate `admin/` entry were removed rather than fixing imports for dead code.

## User preferences
- User wants a complete architectural redesign: modern (non-"AI-generic") UI/UX across frontend and backend, full documentation, and working launch scripts. Scope is large — see the proposed follow-up tasks for how this is broken up. This is the design/product direction to follow for that work: aim for genuinely original, "award-winning fullstack developer" craft rather than a generic template look.
