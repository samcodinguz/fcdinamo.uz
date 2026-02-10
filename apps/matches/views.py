from django.shortcuts import render
from apps.leagues.models import Season
from apps.core.utils import get_base_context
from . import utils

def matches_finished(request, code):

    season = request.GET.get('season')
    seasons = Season.objects.filter(team_type__code=code).order_by('-year')

    if season:
        season = seasons.filter(year=season).first()
    else:
        season = seasons.first()

    matches_finished = utils.get_matches(season, team_type=code, finished=True, order='last', single=False)

    years = Season.objects.filter(team_type__code=code).values_list('year', flat=True).distinct().order_by('-year')

    seasons_year = [
        {
            'year': year,
            'label': year
        }
        for year in years
    ]

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'matches', 'url': 'matches_finished', 'args': [code]},
        {'title': 'finished', 'url': 'matches_finished', 'args': [code]},
        {'title': code, 'url': 'matches_finished', 'args': [code]},
    ]
    context = {
        'grouped_matches': utils.group_matches_by_month(matches_finished),
        'seasons': seasons,
        'seasons_year': seasons_year,
        'current_season': season.year if season else None,
        'page_title': 'Yakunlangan o\'yinlar',
        'paths': paths,
        'men': 'active',
        'finished': 'active',
    }
    context.update(get_base_context(request))

    return render(request, 'matches/finished.html', context)

def matches_upcoming(request, code):

    season = Season.objects.order_by('-year').first()
    matches_upcoming_all = utils.get_matches(season, team_type=code, finished=False, order='last', single=False)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'matches', 'url': 'matches_upcoming', 'args': [code]},
        {'title': 'upcoming', 'url': 'matches_upcoming', 'args': [code]},
        {'title': code, 'url': 'matches_upcoming', 'args': [code]},
    ]
    context = {
        'grouped_matches': utils.group_matches_by_month(matches_upcoming_all),
        'page_title': 'Navbatdagi o\'yinlar',
        'paths': paths,
        'men': 'active',
        'upcoming': 'active',
    }
    context.update(get_base_context(request))

    return render(request, 'matches/upcoming.html', context)