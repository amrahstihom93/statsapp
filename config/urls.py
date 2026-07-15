"""
URL Configuration for statsproject.
Django 4.2 compatible — uses path() and re_path() from django.urls.
"""
from django.urls import path, re_path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Import views from the new app locations
from core import views as core_views
from apps.accounts import views as accounts_views
from apps.accounts import api_views as accounts_api
from apps.datasets import views as dataset_upload_views
from apps.datasets import api_views as datasets_api
from apps.processes import views as process_views
from apps.processes import api_views as processes_api
from apps.analytics import views as analytics_views
from apps.analytics import api_views as analytics_api
from apps.analytics.charts_src import views as chart_views
from apps.machinelearning import views as ml_views
from apps.processmap import views as processmap_views
from apps.qualitytools import views as qualitytools_views

urlpatterns = [
    # ── Core ────────────────────────────────────────────────────────────────
    path('', core_views.home, name='home'),
    path('test/', core_views.hometest, name='main'),
    path('dataset/', core_views.datasetlist, name='datasetlist'),
    path('api/data/', core_views.get_data, name='api-data'),

    # ── Auth ────────────────────────────────────────────────────────────────
    path('signup/', accounts_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('account_activation_sent/', accounts_views.account_activation_sent, name='account_activation_sent'),
    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
        accounts_views.activate,
        name='activate',
    ),
    path('complete_tour/', accounts_views.complete_tour, name='complete_tour'),

    # ── Upload / Dataset ─────────────────────────────────────────────────────
    path('upload/', dataset_upload_views.upload, name='upload'),
    path('makeCol/', dataset_upload_views.makeCol, name='makeCol'),
    path('giveDatasetName/', dataset_upload_views.giveDatasetName, name='give-dataset-name'),
    path('upload/fileType/', dataset_upload_views.submitFiletype, name='submitFiletype'),
    path('upload/dataType/', dataset_upload_views.changeDataType, name='submitDatatype'),
    re_path(r'^delete/(?P<dataset_name>\w+)/$', dataset_upload_views.deleteDataset, name='deleteDataset'),
    path('mysqlconnect/', dataset_upload_views.mysqlconnect, name='mySqlConnector'),

    # ── Charts / Visualization ───────────────────────────────────────────────
    path('charts/', chart_views.chart, name='chart'),
    re_path(r'^chart/(?P<dataset_name>\D+)/$', chart_views.get_visualization, name='visualization'),
    path('saveGraph/', chart_views.saveVisualization, name='save-visualization'),
    path('getVisualization/', chart_views.getVisualizationList, name='get-visualization'),
    re_path(r'^api/chart/data/(?P<dataset_name>\D+)/$', chart_views.visualization_data, name='visualization-data'),
    re_path(r'^api/chart/data/(?P<graph_type>\D+)/(?P<dataset_name>\D+)/$', chart_views.get_data, name='chart-data'),
    re_path(r'^chart/(?P<graph_type>\D+)/(?P<dataset_name>\D+)/$', chart_views.makechart, name='aschart'),
    path('getDataset/', chart_views.getDataset, name='getDataset'),
    path('getGraphFields/', chart_views.getGraphFields, name='getGraphFields'),
    path('getGraphData/', chart_views.getGraphData, name='getGraphData'),
    path('getSubgroup/', chart_views.getSubgroup, name='getSubgroup'),
    path('updateVisualization/', chart_views.editVisualisation, name='editVisualisation'),
    re_path(r'^delVisualization/(?P<id>\d+)/$', chart_views.delVisualization, name='delete-visualization'),

    # ── Process ──────────────────────────────────────────────────────────────
    path('makeProcess/', process_views.makeProcess, name='makeProcess'),
    path('getProcess/', process_views.getProcess, name='getProcess'),
    path('getProcessList/', process_views.getProcessList, name='getProcessList'),

    # ── Statistical / Analytics ──────────────────────────────────────────────
    path('saveStatistics/', analytics_views.saveStatistics, name='saveStatistics'),
    path('calculateStatistics/', analytics_views.calculateStatistics, name='calculateStatistics'),
    path('getStatistical/', analytics_views.getStatisticalList, name='getStatistical'),
    re_path(r'^delStatistical/(?P<id>\d+)/$', analytics_views.delStatistical, name='delete-statistical'),

    path('saveAnalytics/', analytics_views.saveAnalytics, name='saveAnalytics'),
    path('calculateAnalytics/', analytics_views.calculateAnalytics, name='calculateAnalytics'),
    path('getAnalytical/', analytics_views.getAnalyticalList, name='getAnalytical'),
    re_path(r'^delAnalytical/(?P<id>\d+)/$', analytics_views.delAnalytical, name='delete-analytical'),

    path('calculateHypothesis/', analytics_views.calculateHypothesis, name='calculateHypothesis'),
    path('saveHypothesis/', analytics_views.saveHypothesis, name='saveHypothesis'),
    path('hypoList/', analytics_views.hypoList, name='hypoList'),

    # ── Machine Learning ─────────────────────────────────────────────────────
    path('mlearn/', ml_views.mlearn, name='mlearn'),
    path('calcsregression/', ml_views.calcsregression, name='calcsregression'),
    path('multiregression/', ml_views.multiregression, name='multiregression'),
    path('saveMLmodel/', ml_views.saveMLmodel, name='saveMLmodel'),
    path('mlist/', ml_views.mlist, name='mlist'),
    path('mldat/', ml_views.mldat, name='mldat'),
    path('mdep/', ml_views.mlearn, name='mdep'),

    # ── Process Map ───────────────────────────────────────────────────────────
    path('processmap/', processmap_views.processmap, name='processmap'),
    path('open/', processmap_views.processmapopen, name='processmapopen'),
    path('save/', processmap_views.processmapsave, name='save'),

    # ── Quality Tools ─────────────────────────────────────────────────────────
    path('qualityTools/', qualitytools_views.qtools, name='qualitytools'),
    path('opptracker/', qualitytools_views.opptracker, name='opptracker'),
    path('saveFMEA/', qualitytools_views.saveFMEA, name='qualitytools_fmea'),
    path('fmeaList/', qualitytools_views.fmeaList, name='qualitytools_fmeaList'),

    # ── Admin ────────────────────────────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ── API v1 JSON REST endpoints (React connection) ─────────────────────────
    path('api/v1/auth/csrf/', accounts_api.csrf_token_view, name='api-csrf'),
    path('api/v1/auth/me/', accounts_api.me, name='api-me'),
    path('api/v1/auth/login/', accounts_api.login_view, name='api-login'),
    path('api/v1/auth/logout/', accounts_api.logout_view, name='api-logout'),
    path('api/v1/auth/complete-tour/', accounts_api.complete_tour_view, name='api-complete-tour'),
    
    path('api/v1/clients/', accounts_api.clients_view, name='api-clients'),
    path('api/v1/users/', accounts_api.users_view, name='api-users'),
    path('api/v1/users/<int:user_id>/assign-client/', accounts_api.assign_client_view, name='api-assign-client'),
    
    path('api/v1/datasets/', datasets_api.datasets_list_view, name='api-datasets-list'),
    path('api/v1/datasets/upload/', datasets_api.dataset_upload_view, name='api-dataset-upload'),
    path('api/v1/datasets/<str:dataset_id>/preview/', datasets_api.dataset_preview_view, name='api-dataset-preview'),
    path('api/v1/datasets/<str:dataset_id>/', datasets_api.dataset_delete_view, name='api-dataset-delete'),

    path('api/v1/processes/', processes_api.processes_view, name='api-processes'),
    
    path('api/v1/analytics/stats/', analytics_api.stats_list_view, name='api-stats-list'),
    path('api/v1/analytics/analytical/', analytics_api.analytics_list_view, name='api-analytics-list'),
    path('api/v1/analytics/models/', analytics_api.ml_models_view, name='api-ml-models'),
    path('api/v1/analytics/summary/', analytics_api.dashboard_summary_view, name='api-dashboard-summary'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

