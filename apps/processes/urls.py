from django.urls import path
from . import views

urlpatterns = [
    path('makeProcess/', views.makeProcess, name='makeProcess'),
    path('getProcess/', views.getProcess, name='getProcess'),
    path('getProcessList/', views.getProcessList, name='getProcessList'),
]
