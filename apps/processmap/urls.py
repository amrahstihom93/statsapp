from django.urls import path
from . import views

urlpatterns = [
    path('', views.processmap, name='processmap'),
    path('open/', views.processmapopen, name='processmapopen'),
    path('save/', views.processmapsave, name='save'),
]
