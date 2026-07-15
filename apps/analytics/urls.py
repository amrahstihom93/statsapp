from django.urls import path, re_path
from .charts_src import views as chart_views
from . import views

urlpatterns = [
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
    path('saveStatistics/', views.saveStatistics, name='saveStatistics'),
    path('calculateStatistics/', views.calculateStatistics, name='calculateStatistics'),
    path('getStatistical/', views.getStatisticalList, name='getStatistical'),
    re_path(r'^delStatistical/(?P<id>\d+)/$', views.delStatistical, name='delete-statistical'),
    path('saveAnalytics/', views.saveAnalytics, name='saveAnalytics'),
    path('calculateAnalytics/', views.calculateAnalytics, name='calculateAnalytics'),
    path('getAnalytical/', views.getAnalyticalList, name='getAnalytical'),
    re_path(r'^delAnalytical/(?P<id>\d+)/$', views.delAnalytical, name='delete-analytical'),
    path('calculateHypothesis/', views.calculateHypothesis, name='calculateHypothesis'),
    path('saveHypothesis/', views.saveHypothesis, name='saveHypothesis'),
    path('hypoList/', views.hypoList, name='hypoList'),
]
