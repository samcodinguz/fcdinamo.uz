from django.urls import path
from . import views

urlpatterns = [
    path('home', views.judge, name='judge'),
    path('news', views.judge_news, name='judge_news'),
    path('news/edit/<int:news_id>', views.judge_news_edit, name='judge_news_edit'),
]