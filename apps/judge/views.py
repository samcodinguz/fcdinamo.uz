from django.shortcuts import render, redirect, get_object_or_404
from apps.core.utils import get_base_context
from apps.news.models import News, NewsTag, NewsCategory
from apps.core.utils import paginate_queryset
from django.contrib.auth.decorators import login_required
import os

def judge(request):

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
    ]

    context = {
        'paths': paths,
        'page_title': 'Admin sahifasi'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/judge.html', context)


def judge_news(request):

    category = request.GET.get('category')
    status = request.GET.get('status')
    per_page = request.GET.get('per_page', 10)

    news_list = News.objects.all().select_related('category').order_by('-created_at')
    categorys = NewsCategory.objects.all()

    if category and category != "all":
        category = int(category)
        news_list = news_list.filter(category__id=category)

    if status and status != "all":
        if status == "true":
            news_list = news_list.filter(is_published=True)
        elif status == "false":
            news_list = news_list.filter(is_published=False)

    news_list, pagination_range = paginate_queryset(news_list, request, per_page=per_page)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'news', 'url': 'judge_news', 'args': []},
    ]

    context = {
        'categorys': categorys,
        'category': category,
        'status': status,
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        'news_list': news_list,
        'paths': paths,
        'page_title': 'Yangiliklarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/news/news.html', context)

@login_required
def judge_news_edit(request, news_id):

    news = get_object_or_404(News, id=news_id)
    image_name = os.path.basename(news.image.name)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'news', 'url': 'judge_news', 'args': []},
        {'title': 'edit', 'url': 'judge_news_edit', 'args': [news_id]},
        {'title': news_id, 'url': 'judge_news_edit', 'args': [news_id]},
    ]

    context = {
        'news': news,
        "image_name": image_name,
        'paths': paths,
        'page_title': 'Yangiliklarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/news/edit.html', context)