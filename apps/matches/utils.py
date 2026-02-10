from .models import Match
from apps.core.models import MyClub
from django.db.models import Q
from collections import OrderedDict

def get_main_team():
    club = MyClub.objects.select_related('team').first()
    if club and club.team:
        return club.team
    return None

def get_matches(season, team_type=None, finished=None, order='last', single=True):

    if not season:
        return Match.objects.none()
    
    team = get_main_team()
    if not team:
        return Match.objects.none()
    
    result = Match.objects.filter(season__year=season.year).filter(
        Q(home_team=team) | Q(away_team=team)
    ).select_related('home_team', 'away_team', 'season')

    if finished is not None:
        result = result.filter(is_finished=finished)

    if team_type:
        result = result.filter(season__team_type__code=team_type)

    if order == 'last':
        result = result.order_by('-match_date')
    else:
        result = result.order_by('match_date')

    if single:
        return result.first()
    
    return result

def group_matches_by_month(matches):
    MONTHS_UZ = {
        1: "Yanvar",
        2: "Fevral",
        3: "Mart",
        4: "Aprel",
        5: "May",
        6: "Iyun",
        7: "Iyul",
        8: "Avgust",
        9: "Sentyabr",
        10: "Oktyabr",
        11: "Noyabr",
        12: "Dekabr",
    }

    DAYS_UZ = {
        0: "Du",
        1: "Se",
        2: "Ch",
        3: "Pa",
        4: "Ju",
        5: "Sh",
        6: "Ya",
    }

    grouped = OrderedDict()

    for match in matches:
        # --- Kun labelini shu yerda qo‘shamiz ---
        d = match.match_date
        match.day_label = f"{DAYS_UZ[d.weekday()]} {d.day:02d} {MONTHS_UZ[d.month][:3]}"

        key = d.strftime('%Y-%m')
        grouped.setdefault(key, []).append(match)

    # Oy sarlavhalari
    result = OrderedDict()
    for key, value in grouped.items():
        date = value[0].match_date
        month_name = MONTHS_UZ[date.month]
        label = f"{month_name.upper()} {date.year}"
        result[label] = value

    return result