from django.urls import path
from . import views

urlpatterns = [
    path('vedio', views.media_vedio, name='media_vedios')
]