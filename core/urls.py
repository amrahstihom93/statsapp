from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.hometest, name='main'),
    path('dataset/', views.datasetlist, name='datasetlist'),
    path('api/data/', views.get_data, name='api-data'),
]
