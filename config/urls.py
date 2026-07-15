"""
URL Configuration for statsproject.
Django 4.2 compatible — uses path() and re_path() from django.urls.
"""
from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from apps.processmap import views as processmap_views

urlpatterns = [
    # ── Admin ────────────────────────────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ── Process Map is linked as a real page nav (see
    # apps/datasets/templates/datasets/datasetSubmenu: href="processmap"), so
    # it needs an explicit prefixed path — its own urls.py registers '' for
    # this view, expecting to be included at a prefix. Quality Tools, by
    # contrast, is only ever opened via an in-page Angular hash route
    # (#qualityTools) inside the dataset workspace, which loads a static
    # partial — no real Django page exists for it, so no route is added here.
    path('processmap/', processmap_views.processmap, name='processmap'),

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

