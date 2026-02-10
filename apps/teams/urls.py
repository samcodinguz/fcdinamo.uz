from django.urls import path
from . import views

urlpatterns = [
    path('managements', views.managements, name='managements'),
    path('coaches', views.coaches, name='coaches'),
    path('players/<str:team_type>', views.players, name='players'),

    path('management/<int:id>', views.management_detail, name='management_detail'),
    path('coach/<int:id>', views.coach_detail, name='coach_detail'),
    path('players/<str:team_type>/<int:player_id>', views.players_detail, name='player_detail'),
]