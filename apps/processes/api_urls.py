from django.urls import path
from . import api_views

urlpatterns = [
    path('', api_views.processes_view, name='api-processes'),
]
