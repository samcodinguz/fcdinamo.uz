from django.shortcuts import render
from apps.leagues.models import Season
from apps.core.utils import get_base_context
from . import utils

def matches_finished_mens(request):

    season = request.GET.get('season')
    seasons = Season.objects.filter(team_type='men').order_by('-year')

    if season:
        season = seasons.filter(year=season).first()
    else:
        season = seasons.first()

    matches_finished_men = utils.get_matches(season, team_type='men', finished=True, order='last', single=False)

    years = Season.objects.filter(team_type='men').values_list('year', flat=True).distinct().order_by('-year')

    seasons_year = [
        {
            'year': year,
            'label': f'{year}/{(year+1)%100}'
        }
        for year in years
    ]

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'matches', 'url': 'matches_finished_mens', 'args': []},
        {'title': 'finished', 'url': 'matches_finished_mens', 'args': []},
        {'title': 'mens', 'url': 'matches_finished_mens', 'args': []},
    ]
    context = {
        'grouped_matches': utils.group_matches_by_month(matches_finished_men),
        'seasons': seasons,
        'seasons_year': seasons_year,
        'current_season': season.year if season else None,
        'page_title': 'Yakunlangan o\'yinlar',
        'paths': paths,
        'men': 'active',
        'finished': 'active',
    }
    context.update(get_base_context(request))

    return render(request, 'matches/finished/men.html', context)

def matches_finished_womens(request):

    season = request.GET.get('season')
    seasons = Season.objects.filter(team_type='women').order_by('-year')

    if season:
        season = seasons.filter(year=season).first()
    else:
        season = seasons.first()

    matches_finished_women = utils.get_matches(season, team_type='women', finished=True, order='last', single=False)
    years = Season.objects.filter(team_type='women').values_list('year', flat=True).distinct().order_by('-year')

    seasons_year = [
        {
            'year': year,
            'label': f'{year}/{(year+1)%100}'
        }
        for year in years
    ]

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'matches', 'url': 'matches_finished_womens', 'args': []},
        {'title': 'finished', 'url': 'matches_finished_womens', 'args': []},
        {'title': 'womens', 'url': 'matches_finished_womens', 'args': []},
    ]
    context = {
        'grouped_matches': utils.group_matches_by_month(matches_finished_women),
        'seasons': seasons,
        'seasons_year': seasons_year,
        'current_season': season.year if season else None,
        'page_title': 'Yakunlangan o\'yinlar',
        'paths': paths,
        'women': 'active',
        'finished': 'active',
    }
    context.update(get_base_context(request))

    return render(request, 'matches/finished/women.html', context)

def matches_upcoming_mens(request):

    season = Season.objects.order_by('-year').first()
    matches_upcoming_all = utils.get_matches(season, team_type='men', finished=False, order='last', single=False)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'matches', 'url': 'matches_upcoming_mens', 'args': []},
        {'title': 'upcoming', 'url': 'matches_upcoming_mens', 'args': []},
        {'title': 'mens', 'url': 'matches_upcoming_mens', 'args': []},
    ]
    context = {
        'grouped_matches': utils.group_matches_by_month(matches_upcoming_all),
        'page_title': 'Navbatdagi o\'yinlar',
        'paths': paths,
        'men': 'active',
        'upcoming': 'active',
    }
    context.update(get_base_context(request))

    return render(request, 'matches/upcoming/men.html', context)

def matches_upcoming_womens(request):

    season = Season.objects.order_by('-year').first()
    matches_upcoming_all = utils.get_matches(season, team_type='women', finished=False, order='last', single=False)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'matches', 'url': 'matches_upcoming_womens', 'args': []},
        {'title': 'upcoming', 'url': 'matches_upcoming_womens', 'args': []},
        {'title': 'womens', 'url': 'matches_upcoming_womens', 'args': []},
    ]
    context = {
        'grouped_matches': utils.group_matches_by_month(matches_upcoming_all),
        'page_title': 'Navbatdagi o\'yinlar',
        'paths': paths,
        'women': 'active',
        'upcoming': 'active',
    }
    context.update(get_base_context(request))

    return render(request, 'matches/upcoming/women.html', context)