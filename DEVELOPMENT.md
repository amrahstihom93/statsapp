# Sigma Statistics Development Guide

Welcome to the Sigma Statistics development documentation. This guide is intended for code managers and developers looking to extend the platform's capabilities, add new features, or expose new APIs.

## Architecture Overview

Sigma Statistics uses a hybrid Django (Backend) + Angular (Frontend) architecture.

- **Backend**: Django handles authentication (`apps/accounts`), routing, and API endpoints for data processing.
- **Frontend (Legacy/Dashboards)**: Django Templates (`core/templates`) are used for landing pages, authentication views, and the dashboard root view.
- **Frontend (Workspace)**: AngularJS handles the interactive workspaces (Datasets, Process Maps, Visualizations) via SPA routing inside `apps/datasets/templates/datasets/datasetlist.html`.
- **Styling**: The application utilizes a customized dark mode aesthetic inspired by Awwwards-winning designs, utilizing CSS Variables, Glassmorphism, and modern typography (Archivo Black/Inter).

---

## Adding a New Feature (Frontend App)

To add a new tool or workspace module (e.g., a new "Advanced Analytics" module):

### 1. Update the Sidebar Navigation

The sidebar is located in `apps/datasets/templates/datasets/datasetlist.html`. Add your new navigation item using the standard glassmorphic sidebar classes:

```html
<div class="sidebar-nav-item">
    <a href="#advancedAnalytics" class="sidebar-nav-link" data-toggle="collapse" aria-expanded="false">
        <i class="fas fa-microchip"></i>
        <span>Advanced Analytics</span>
    </a>
    <ul class="collapse sidebar-submenu" id="advancedAnalytics">
        <li><a href="#/newModule">Launch Module</a></li>
    </ul>
</div>
```

### 2. Register the Angular Route

Update the `app.js` (or relevant Angular routing module in `static/js/app.js`) to point to your new template:

```javascript
$routeProvider.when('/newModule', {
    templateUrl: '/static/templates/new_module.html',
    controller: 'NewModuleController'
});
```

### 3. Build the Template

Create your HTML template (e.g., `new_module.html`) in the designated static folder. Ensure you wrap your content in the standard workspace container:

```html
<div class="workspace-content">
    <h2>Advanced Analytics</h2>
    <!-- Module content -->
</div>
```

---

## Creating a New API Endpoint

To create a new data processing or utility API endpoint in Django:

### 1. Define the View

Create a new view function or class in the appropriate `views.py` (e.g., `core/views.py` or a dedicated app view). Use Django's `JsonResponse` for API responses.

```python
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
def advanced_analysis_api(request):
    try:
        data = json.loads(request.body)
        # Perform computation...
        result = {"status": "success", "score": 98.5}
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
```

### 2. Register the URL

Add the route to the relevant `urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    # ... existing routes ...
    path('api/v1/advanced-analysis/', views.advanced_analysis_api, name='advanced_analysis'),
]
```

### 3. Consume the API in Angular

Use `$http` to call your new API from your Angular controller:

```javascript
app.controller('NewModuleController', function($scope, $http) {
    $scope.runAnalysis = function(payload) {
        $http.post('/api/v1/advanced-analysis/', payload)
            .then(function(response) {
                $scope.result = response.data.score;
            })
            .catch(function(error) {
                console.error("Analysis failed", error);
            });
    };
});
```

---

## Styling Guidelines (The "Sigma" Aesthetic)

When adding new components, adhere to the core design tokens to maintain the premium Awwwards-style look:

- **Colors**:
  - Backgrounds: `#050505` (Deep Black)
  - Cards/Panels: `rgba(255, 255, 255, 0.03)` with `rgba(255,255,255,0.05)` borders
  - Primary Accent: `#ccff00` (Neon Lime)
  - Text Primary: `#f4f4f5`
  - Text Secondary: `#a1a1aa`
- **Typography**:
  - Headings (H1-H4): `Archivo Black` (Weight 400, letter-spacing 1px)
  - Body Text: `Inter` (Weights 300, 400, 500)
- **Effects**:
  - Use `backdrop-filter: blur(15px)` for sticky headers or overlapping UI elements.
  - Apply subtle translateY(-5px) micro-animations on hover for interactive elements.

> [!TIP]
> Always verify new modules in dark mode. The application does not currently support a light mode theme; contrast relies on neon accents against deep blacks.

---

## Integration Checklist for Code Managers

Before merging a new feature branch:

- [ ] **Routing Check**: Does the new route conflict with existing Django or Angular routes?
- [ ] **CSRF Verification**: If submitting POST requests from Angular to Django, ensure the `X-CSRFToken` header is included.
- [ ] **Design Review**: Does the feature utilize the custom cursor and Awwwards styling tokens?
- [ ] **Responsive Validation**: Ensure grids degrade gracefully on mobile/tablet viewports.
