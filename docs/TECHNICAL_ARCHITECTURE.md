# Technical Architecture

## 1. Stack & Overview
StatsApp is built on standard, modern web technologies:
- **Backend**: Django 4.2+ (Python 3.11+)
- **Database**: SQLite (for local development/POC) / PostgreSQL (for production). MongoEngine has been deprecated in favor of native Django ORM models.
- **Frontend**: Django Templates, Bootstrap 4, AngularJS 1.2 (legacy frontend logic for dashboards).
- **Charting**: D3.js, Chart.js.

## 2. Django Application Structure
The repository follows a modern modularized Django structure.

```text
statsapp/
├── apps/                    # All modular Django applications
│   ├── accounts/            # Authentication, User Profiles, JWT Tokens
│   ├── analytics/           # Statistics (Mean/ANOVA) & Charting logic
│   ├── datasets/            # File uploads (CSV/Excel) and parsing
│   ├── machinelearning/     # Regression models
│   ├── processes/           # Process tracking & metadata
│   ├── processmap/          # Flowchart building
│   └── qualitytools/        # FMEA & Opportunity Tracker
├── core/                    # Base templates, homepage views, shared utilities
├── config/                  # Global Django settings (formerly statsproject)
│   ├── settings/
│   │   ├── base.py          # Shared settings
│   │   ├── local.py         # Local development settings
│   │   └── production.py    # Production overrides
│   ├── urls.py              # Root URL router
│   └── wsgi.py              # WSGI entrypoint
├── docs/                    # Documentation
├── media/                   # User-uploaded files (CSVs)
├── static/                  # Global static assets
│   ├── css/
│   ├── js/
│   │   ├── app/             # Custom application scripts
│   │   ├── partials/        # AngularJS HTML templates
│   │   └── vendor/          # Bootstrap, jQuery, D3, etc.
│   └── img/
└── manage.py
```

## 3. Data Model & Architecture Decisions
- **Namespacing**: Apps are strictly namespaced under the `apps` package. Example import: `from apps.accounts.models import Profile`.
- **Templates**: Are stored within each app (`apps/<app_name>/templates/<app_name>/`) ensuring no collision between template names across apps. Shared layouts reside in `core/templates/core/`.
- **Database Standardization**: Legacy MongoEngine dependencies have been fully removed. The application relies entirely on standard relational databases natively supported by Django.

## 4. Setting up Local POC Environment
To run the platform locally, follow these steps:

1. **Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Database & Migrations**:
   The `bootstrap_dev.py` script automatically migrates the database and creates the necessary base entities (Admin User, Root Process).
   ```bash
   export DJANGO_SETTINGS_MODULE=config.settings.local
   python manage.py makemigrations
   python manage.py migrate
   python bootstrap_dev.py
   ```
   *Note: This generates a `db.sqlite3` file and seeds the `admin` account with password `admin123`.*

3. **Running the Server**:
   ```bash
   python manage.py runserver 8000
   ```
   Navigate to `http://127.0.0.1:8000/` in your browser.
