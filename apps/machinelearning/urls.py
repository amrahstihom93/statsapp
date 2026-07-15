from django.urls import path
from . import views

urlpatterns = [
    path('mlearn/', views.mlearn, name='mlearn'),
    path('calcsregression/', views.calcsregression, name='calcsregression'),
    path('multiregression/', views.multiregression, name='multiregression'),
    path('saveMLmodel/', views.saveMLmodel, name='saveMLmodel'),
    path('mlist/', views.mlist, name='mlist'),
    path('mldat/', views.mldat, name='mldat'),
]
