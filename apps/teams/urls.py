from django.urls import path
from . import views

urlpatterns = [
    path('managements', views.managements, name='managements'),
    path('coaches', views.coaches, name='coaches'),
    path('players/mens', views.mens, name='mens'),
    path('players/womens', views.womens, name='womens'),
]