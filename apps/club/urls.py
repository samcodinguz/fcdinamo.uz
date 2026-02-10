from django.urls import path
from . import views

urlpatterns = [
    path('history', views.club_history, name='club_history'),
    path('achievements', views.club_achievements, name='club_achievements'),
    path('stadium', views.club_stadium, name='club_stadium'),
]