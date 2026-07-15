from django.urls import path, re_path
from . import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('makeCol/', views.makeCol, name='makeCol'),
    path('giveDatasetName/', views.giveDatasetName, name='give-dataset-name'),
    path('upload/fileType/', views.submitFiletype, name='submitFiletype'),
    path('upload/dataType/', views.changeDataType, name='submitDatatype'),
    re_path(r'^delete/(?P<dataset_name>\w+)/$', views.deleteDataset, name='deleteDataset'),
    path('mysqlconnect/', views.mysqlconnect, name='mySqlConnector'),
]
