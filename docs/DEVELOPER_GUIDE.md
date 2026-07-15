# Developer Guide

## 1. Creating a New Application
StatsApp enforces a modular structure. All domain-specific logic must be contained within isolated apps.

To create a new app (e.g., `forecasting`):
1. **Generate the App**:
   Navigate to the `apps/` directory and run:
   ```bash
   python ../manage.py startapp forecasting
   ```
2. **Update `apps.py`**:
   Ensure the `name` attribute reflects the namespaced path:
   ```python
   # apps/forecasting/apps.py
   from django.apps import AppConfig

   class ForecastingConfig(AppConfig):
       default_auto_field = 'django.db.models.BigAutoField'
       name = 'apps.forecasting'
   ```
3. **Register App**:
   Add `'apps.forecasting'` to `INSTALLED_APPS` in `config/settings/base.py`.
4. **Register URLs**:
   Include the new app's URLs in `config/urls.py`:
   ```python
   path('forecasting/', include('apps.forecasting.urls')),
   ```

## 2. Template Conventions
To avoid template collision across apps, all templates must be stored inside a subdirectory matching the app's name:

**Correct Layout:**
`apps/datasets/templates/datasets/datasetlist.html`

**Usage in View:**
```python
def dataset_view(request):
    return render(request, 'datasets/datasetlist.html')
```

If you need to extend the base layout, reference the `core` app:
```html
{% extends "core/base.html" %}
```

## 3. Static Files & Frontend Assets
- Global static assets (e.g., CSS libraries, third-party JS) should be placed in the root `static/` directory.
- **Third-Party Vendors**: Place inside `static/js/vendor/` or `static/css/vendor/`.
- **Angular Templates**: AngularJS partials should be stored in `static/js/partials/` and referenced via absolute or relative URL in the AngularJS routing config.

## 4. Linting and Code Quality
- Ensure all relative cross-app imports use absolute paths (`from apps.datasets.models import Dataset`). Do not use implicit relative imports.
- Use `python manage.py check` routinely to identify dangling views or template errors.
- Always run `python manage.py makemigrations` and commit the generated migration files when modifying models.

## 5. Security Note
- Never commit the `.env` file containing database passwords and secret keys.
- Ensure all user-facing views utilize Django's `@login_required` decorator unless explicitly designed as public endpoints.
