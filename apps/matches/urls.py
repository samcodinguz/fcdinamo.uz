from django.urls import path
from . import views

urlpatterns = [
    path('finished/<str:code>', views.matches_finished, name='matches_finished'),
    path('upcoming/<str:code>', views.matches_upcoming, name='matches_upcoming'),
]