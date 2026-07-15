from django.urls import path
from . import api_views

urlpatterns = [
    path('csrf/', api_views.csrf_token_view, name='api-csrf'),
    path('me/', api_views.me, name='api-me'),
    path('login/', api_views.login_view, name='api-login'),
    path('logout/', api_views.logout_view, name='api-logout'),
    path('complete-tour/', api_views.complete_tour_view, name='api-complete-tour'),
    path('clients/', api_views.clients_view, name='api-clients'),
    path('users/', api_views.users_view, name='api-users'),
    path('users/<int:user_id>/assign-client/', api_views.assign_client_view, name='api-assign-client'),
]
