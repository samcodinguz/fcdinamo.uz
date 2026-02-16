from .models import News
from django.db.models import F
from apps.leagues.models import Season
from apps.matches.utils import get_matches
from django.shortcuts import render, get_object_or_404
from apps.core.utils import get_base_context, paginate_queryset
from apps.leagues.models import TeamType

def news_all(request):

    tag_name = request.GET.get('tag')
    news_list = News.objects.filter(is_published=True).select_related('category').order_by('-created_at')
    
    if tag_name:
        news_list = news_list.filter(tags__name=tag_name)
    
    news_list, pagination_range = paginate_queryset(news_list, request, per_page=5)

    season = Season.objects.order_by('-year').first()
    next_men_match = get_matches(season, team_type='men', finished=False, order='first', single=True)
    next_women_match = get_matches(season, team_type='women', finished=False, order='first', single=True)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'news', 'url': 'news_all', 'args': []},
    ]

    context = {
        'news_list': news_list,
        'pagination_range': pagination_range,
        'next_men_match': next_men_match,
        'next_women_match': next_women_match,
        'page_title': 'Barcha yangiliklar',
        'paths': paths,
        'tag_name': tag_name,
    }
    context.update(get_base_context(request))
    return render(request, 'news/news.html', context)

def news(request, code):

    team_type = TeamType.objects.filter(code=code).first()

    news_list = News.objects.filter(is_published=True, category__code=code).select_related('category').order_by('-created_at')
    news_list, pagination_range = paginate_queryset(news_list, request, per_page=5)

    season = Season.objects.order_by('-year').first()
    next_men_match = get_matches(season, team_type='men', finished=False, order='first', single=True)
    next_women_match = get_matches(season, team_type='women', finished=False, order='first', single=True)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'news', 'url': 'news', 'args': [code]},
        {'title': code, 'url': 'news', 'args': [code]},
    ]

    context = {
        'news_list': news_list,
        'pagination_range': pagination_range,
        'next_men_match': next_men_match,
        'next_women_match': next_women_match,
        'page_title': f"{team_type.name} yangiliklari",
        'paths': paths,
    }
    context.update(get_base_context(request))
    return render(request, f'news/news.html', context)

def news_detail(request, news_detail_id):

    if request.user.is_superuser:
        news_detail = get_object_or_404(News.objects.select_related('category', 'author').prefetch_related('tags'), pk=news_detail_id)
    else:
        news_detail = get_object_or_404(News.objects.select_related('category', 'author').prefetch_related('tags'), pk=news_detail_id, is_published=True)
    News.objects.filter(pk=news_detail.pk).update(
        views_count=F('views_count') + 1
    )

    related_news = (News.objects.filter(is_published=True, category=news_detail.category).exclude(pk=news_detail.pk).select_related('category').order_by('?')[:4])
    most_viewed_news = (News.objects.filter(is_published=True).exclude(pk=news_detail.pk).order_by('-views_count')[:4])
    
    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'news', 'url': 'news_all', 'args': []},
        {'title': news_detail.category.code, 'url': 'news', 'args': [news_detail.category.code]},
        {'title': news_detail_id, 'url': 'news_detail', 'args': [news_detail_id]},
    ]

    context = {
        'news_detail': news_detail,
        'related_news': related_news,
        'most_viewed_news': most_viewed_news,
        'page_title': news_detail.category.name,
        'paths': paths,
    }

    context.update(get_base_context(request))

    return render(request, 'news/detail.html', context)