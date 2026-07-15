"""
URL Configuration for statsproject.
Django 4.2 compatible — uses path() and re_path() from django.urls.
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ── Admin ────────────────────────────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ── App routes (each app owns its own urls.py, included below) ──────────
    path('', include('core.urls')),
    path('', include('apps.accounts.urls')),
    path('', include('apps.datasets.urls')),
    path('', include('apps.analytics.urls')),
    path('', include('apps.processes.urls')),
    path('', include('apps.machinelearning.urls')),
    path('', include('apps.processmap.urls')),
    path('', include('apps.qualitytools.urls')),
    path('api/v1/auth/', include('apps.accounts.api_urls')),
    path('api/v1/datasets/', include('apps.datasets.api_urls')),
    path('api/v1/processes/', include('apps.processes.api_urls')),
    path('api/v1/analytics/', include('apps.analytics.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

