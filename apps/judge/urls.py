from django.urls import path
from . import views

urlpatterns = [
    path('home', views.judge, name='judge'),
    path('news', views.judge_news, name='judge_news'),
    path('news/tags', views.judge_news_tags, name='judge_news_tags'),
    path('news/tags/add', views.judge_news_tags_add, name='judge_news_tags_add'),
    path('news/tags/edit/<int:tags_id>', views.judge_news_tags_edit, name='judge_news_tags_edit'),
    path('news/tags/delete/<int:tags_id>', views.judge_news_tags_delete, name='judge_news_tags_delete'),
    path('news/edit/<int:news_id>', views.judge_news_edit, name='judge_news_edit'),
    path('news/edit/add', views.judge_news_add, name='judge_news_add'),
    path('news/delete/<int:news_id>', views.judge_news_delete, name='judge_news_delete'),
]