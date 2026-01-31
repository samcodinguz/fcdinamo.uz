from django.shortcuts import render
from apps.core.utils import get_base_context
from apps.leagues.models import Season
from apps.matches.utils import get_main_team
from apps.leagues.utils import get_last_season
from apps.leagues.utils import get_active_leagues
from . import utils

def standings_mens(request):

    league_id = request.GET.get("league")

    # Aktiv erkaklar season
    last_men_season = get_last_season(team_type='men')

    # Aktiv ligalar
    leagues = get_active_leagues('men')
    
    # Agar league tanlangan bo‘lsa
    if league_id:
        season = Season.objects.filter(is_active=True, team_type='men', league__id=league_id).select_related('league').first()
    else:
        season = last_men_season
    
    league = None
    if season:
        league = season.league

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'standings', 'url': 'standings_mens', 'args': []},
        {'title': 'mens', 'url': 'standings_mens', 'args': []},
    ]
    context = {
        'table': utils.get_all_standings(season),
        'my_team': get_main_team().team,
        'leagues': leagues,
        'league': league,
        'season': season,
        'page_title': f'Erkaklar {season} natijalar jadvali',
        'paths': paths,
        'men': 'active'
    }
    context.update(get_base_context(request))

    return render(request, 'standings/men.html', context)

def standings_womens(request):

    league_id = request.GET.get("league")

    # Aktiv ayollar season
    last_women_season = get_last_season('women')

    # Aktiv ligalar
    leagues = get_active_leagues('women')
    
    # Agar league tanlangan bo‘lsa
    if league_id:
        season = Season.objects.filter(is_active=True, team_type='women', league__id=league_id).select_related('league').first()
    else:
        season = last_women_season

    league = None
    if season:
        league = season.league

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'standings', 'url': 'standings_womens', 'args': []},
        {'title': 'womens', 'url': 'standings_womens', 'args': []},
    ]
    context = {
        'table': utils.get_all_standings(season),
        'my_team': get_main_team().team,
        'leagues': leagues,
        'league': league,
        'season': season,
        'page_title': f'Ayollar {season} natijalar jadvali',
        'paths': paths,
        'women': 'active',
        'standings': 'active',
    }
    context.update(get_base_context(request))

    return render(request, 'standings/women.html', context)