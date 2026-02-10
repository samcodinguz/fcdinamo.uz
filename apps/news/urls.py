from django.urls import path
from . import views

urlpatterns = [
    path('all', views.news_all, name='news_all'),
    path('<str:code>', views.news, name='news'),
    path('detail/<int:news_detail_id>', views.news_detail, name='news_detail'),
]