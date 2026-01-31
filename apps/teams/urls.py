from django.urls import path
from . import views

urlpatterns = [
    path('managements', views.managements, name='managements'),
    path('coaches', views.coaches, name='coaches'),
    path('players/mens', views.mens, name='mens'),
    path('players/womens', views.womens, name='womens'),

    path('management/<int:id>', views.management_detail, name='management_detail'),
    path('coach/<int:id>', views.coach_detail, name='coach_detail'),
    path('players/men/<int:id>', views.men_detail, name='men_detail'),
    path('players/women/<int:id>', views.women_detail, name='women_detail'),
]