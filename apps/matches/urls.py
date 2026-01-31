from django.urls import path
from . import views

urlpatterns = [
    path('finished/mens', views.matches_finished_mens, name='matches_finished_mens'),
    path('finished/womens', views.matches_finished_womens, name='matches_finished_womens'),
    path('upcoming/mens', views.matches_upcoming_mens, name='matches_upcoming_mens'),
    path('upcoming/womens', views.matches_upcoming_womens, name='matches_upcoming_womens'),
]