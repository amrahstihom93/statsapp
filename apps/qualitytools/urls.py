from django.urls import path
from . import views

urlpatterns = [
    path('', views.qtools, name='qualitytools'),
    path('opptracker/', views.opptracker, name='opptracker'),
    path('saveFMEA/', views.saveFMEA, name='qualitytools_fmea'),
    path('fmeaList/', views.fmeaList, name='qualitytools_fmeaList'),
]
