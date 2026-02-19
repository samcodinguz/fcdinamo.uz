from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contacts', views.contacts, name='contacts'),
    path('sign-in', views.sign_in, name='sign-in'),
    path('sign-up', views.sign_up, name='sign-up'),
    path('sign-out', views.sign_out, name='sign-out'),
    path('video', views.galery_video, name='galery_video'),
    path('photo', views.galery_photo, name='galery_photo'),
    path('search', views.search, name='search'),
]