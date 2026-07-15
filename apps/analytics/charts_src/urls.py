from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.chart, name='chart'),
    re_path(r'^chart/(?P<dataset_name>\D+)/$', views.get_visualization, name='visualization'),
    path('saveGraph/', views.saveVisualization, name='save-visualization'),
    path('getVisualization/', views.getVisualizationList, name='get-visualization'),
    re_path(r'^api/chart/data/(?P<dataset_name>\D+)/$', views.visualization_data, name='visualization-data'),
    re_path(r'^api/chart/data/(?P<graph_type>\D+)/(?P<dataset_name>\D+)/$', views.get_data, name='chart-data'),
    re_path(r'^chart/(?P<graph_type>\D+)/(?P<dataset_name>\D+)/$', views.makechart, name='aschart'),
    path('getDataset/', views.getDataset, name='getDataset'),
    path('getGraphFields/', views.getGraphFields, name='getGraphFields'),
    path('getGraphData/', views.getGraphData, name='getGraphData'),
    path('getSubgroup/', views.getSubgroup, name='getSubgroup'),
    path('updateVisualization/', views.editVisualisation, name='editVisualisation'),
    re_path(r'^delVisualization/(?P<id>\d+)/$', views.delVisualization, name='delete-visualization'),
]
