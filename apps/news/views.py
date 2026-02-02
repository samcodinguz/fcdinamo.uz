from .models import News
from django.db.models import F
from apps.leagues.models import Season
from apps.matches.utils import get_matches
from django.shortcuts import render, get_object_or_404
from apps.core.utils import get_base_context, paginate_queryset

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

def news_mens(request):

    news_list = News.objects.filter(is_published=True, category__id=1).select_related('category').order_by('-created_at')
    news_list, pagination_range = paginate_queryset(news_list, request, per_page=5)

    season = Season.objects.order_by('-year').first()
    next_men_match = get_matches(season, team_type='men', finished=False, order='first', single=True)
    next_women_match = get_matches(season, team_type='women', finished=False, order='first', single=True)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'news', 'url': 'news_all', 'args': []},
        {'title': 'mens', 'url': 'news_mens', 'args': []},
    ]

    context = {
        'news_list': news_list,
        'pagination_range': pagination_range,
        'next_men_match': next_men_match,
        'next_women_match': next_women_match,
        'page_title': "Erkaklar jamoasi yangiliklari",
        'paths': paths,
    }
    context.update(get_base_context(request))
    return render(request, 'news/mens.html', context)

def news_womens(request):

    news_list = News.objects.filter(is_published=True, category__id=2).select_related('category').order_by('-created_at')
    news_list, pagination_range = paginate_queryset(news_list, request, per_page=5)

    season = Season.objects.order_by('-year').first()
    next_men_match = get_matches(season, team_type='men', finished=False, order='first', single=True)
    next_women_match = get_matches(season, team_type='women', finished=False, order='first', single=True)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'news', 'url': 'news_all', 'args': []},
        {'title': 'womens', 'url': 'news_womens', 'args': []},
    ]

    context = {
        'news_list': news_list,
        'pagination_range': pagination_range,
        'next_men_match': next_men_match,
        'next_women_match': next_women_match,
        'page_title': "Ayollar jamoasi yangiliklari",
        'paths': paths,
    }
    context.update(get_base_context(request))
    return render(request, 'news/womens.html', context)

def news_academy(request):

    news_list = News.objects.filter(is_published=True, category__id=3).select_related('category').order_by('-created_at')
    news_list, pagination_range = paginate_queryset(news_list, request, per_page=5)

    season = Season.objects.order_by('-year').first()
    next_men_match = get_matches(season, team_type='men', finished=False, order='first', single=True)
    next_women_match = get_matches(season, team_type='women', finished=False, order='first', single=True)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'news', 'url': 'news_all', 'args': []},
        {'title': 'academy', 'url': 'news_academy', 'args': []},
    ]

    context = {
        'news_list': news_list,
        'pagination_range': pagination_range,
        'next_men_match': next_men_match,
        'next_women_match': next_women_match,
        'page_title': "Akademiya yangiliklari",
        'paths': paths,
    }
    context.update(get_base_context(request))
    return render(request, 'news/academy.html', context)

def news_club(request):

    news_list = News.objects.filter(is_published=True, category__id=4).select_related('category').order_by('-created_at')
    news_list, pagination_range = paginate_queryset(news_list, request, per_page=5)

    season = Season.objects.order_by('-year').first()
    next_men_match = get_matches(season, team_type='men', finished=False, order='first', single=True)
    next_women_match = get_matches(season, team_type='women', finished=False, order='first', single=True)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'news', 'url': 'news_all', 'args': []},
        {'title': 'club', 'url': 'news_club', 'args': []},
    ]

    context = {
        'news_list': news_list,
        'pagination_range': pagination_range,
        'next_men_match': next_men_match,
        'next_women_match': next_women_match,
        'page_title': "Klub yangiliklari",
        'paths': paths,
    }
    context.update(get_base_context(request))
    return render(request, 'news/club.html', context)


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

    title_news = ['mens', 'womens', 'academy', 'club'][news_detail.category.id-1]
    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'news', 'url': 'news_all', 'args': []},
        {'title': title_news, 'url': f'news_{title_news}', 'args': []},
        {'title': news_detail_id, 'url': 'news_detail', 'args': [news_detail_id]},
    ]

    context = {
        'news_detail': news_detail,
        'related_news': related_news,
        'most_viewed_news': most_viewed_news,
        'page_title': news_detail.title,
        'paths': paths,
    }

    context.update(get_base_context(request))

    return render(request, 'news/detail.html', context)