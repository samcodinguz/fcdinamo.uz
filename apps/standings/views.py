from django.shortcuts import render
from apps.core.utils import get_base_context
from apps.leagues.models import Season
from apps.matches.utils import get_main_team
from apps.leagues.utils import get_last_season
from apps.leagues.utils import get_active_leagues
from . import utils

def standings(request, code):

    league_id = request.GET.get("league")

    last_men_season = get_last_season(team_type=code)
    leagues = get_active_leagues(code)
    
    # Agar league tanlangan bo‘lsa
    if league_id:
        season = Season.objects.filter(is_active=True, team_type__code=code, league__id=league_id).select_related('league').first()
    else:
        season = last_men_season
    
    league = None
    if season:
        league = season.league

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'standings', 'url': 'standings', 'args': [code]},
        {'title': code, 'url': 'standings', 'args': [code]},
    ]
    context = {
        'table': utils.get_all_standings(season),
        'my_team': get_main_team(),
        'leagues': leagues,
        'league': league,
        'season': season,
        'page_title': 'Natijalar jadvali',
        'paths': paths,
        'men': 'active'
    }
    context.update(get_base_context(request))

    return render(request, 'standings/standings.html', context)