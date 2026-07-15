from django.urls import path
from . import api_views

urlpatterns = [
    path('stats/', api_views.stats_list_view, name='api-stats-list'),
    path('analytical/', api_views.analytics_list_view, name='api-analytics-list'),
    path('models/', api_views.ml_models_view, name='api-ml-models'),
    path('summary/', api_views.dashboard_summary_view, name='api-dashboard-summary'),
]
