from .models import Season, League

# Erkaklar yoki ayollarni oxirgi seasonini aniqlaydi
def get_last_season(team_type='men'):
    last_sesason = Season.objects.filter(
        is_active=True, team_type=team_type
    ).order_by('-year').first()
    return last_sesason
    
# Erkaklar yoki ayollarni oxirgi season yil raqamini aniqlaydi
def get_last_season_year(team_type='men'):
    season = get_last_season(team_type)
    return season.year if season else None

# Aktiv mavsumdagi ligalarni qaytaradi
def get_active_leagues(team_type):
    return League.objects.filter(
        season__is_active=True, 
        season__team_type=team_type
    ).distinct().order_by('name')