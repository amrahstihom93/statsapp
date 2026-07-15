from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.datasets_list_view, name='api-datasets-list'),
    path('upload/', api_views.dataset_upload_view, name='api-dataset-upload'),
    path('<str:dataset_id>/preview/', api_views.dataset_preview_view, name='api-dataset-preview'),
    path('<str:dataset_id>/', api_views.dataset_delete_view, name='api-dataset-delete'),
]
