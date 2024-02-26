from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # Correct import statement

urlpatterns = [
    # Define your URL patterns here
    path("", views.home, name="home"),
    path('players/', views.player_list, name='players_list'),
    path('players/<int:player_id>/', views.player_profile, name='player_profile')
]
