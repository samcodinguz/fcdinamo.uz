from django.urls import path
from . import views

urlpatterns = [
    path('mens', views.standings_mens, name='standings_mens'),
    path('womens', views.standings_womens, name='standings_womens'),
]