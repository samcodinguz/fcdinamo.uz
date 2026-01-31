from django.urls import path
from . import views

urlpatterns = [
    path('all', views.news_all, name='news_all'),
    path('mens', views.news_mens, name='news_mens'),
    path('womens', views.news_womens, name='news_womens'),
    path('academy', views.news_academy, name='news_academy'),
    path('club', views.news_club, name='news_club'),
    path('<int:news_detail_id>', views.news_detail, name='news_detail'),
]