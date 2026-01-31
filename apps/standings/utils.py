from django.db.models import Q
from apps.leagues.models import Season
from apps.matches.models import Match
from apps.teams.models import Team

def get_last_5_results(season, team):

    matches = Match.objects.filter(is_finished=True, season=season).filter(
        Q(home_team=team) | Q(away_team=team)
    ).order_by('-match_date')[:5]

    results = []

    for match in matches:
        if match.home_team == team:
            gf = match.home_goals
            ga = match.away_goals
        else:
            gf = match.away_goals
            ga = match.home_goals

        if gf > ga:
            results.append('W')
        elif gf == ga:
            results.append('D')
        else:
            results.append('L')

    return results[::-1]  # eski → yangi tartib


def get_form_trend(season, team):

    matches = Match.objects.filter(
        is_finished=True,
        season=season
    ).filter(
        Q(home_team=team) | Q(away_team=team)
    ).order_by('match_date')

    total = matches.count()

    if total < 6:
        return 0  # yetarli data yo‘q

    matches = list(matches)

    prev_5 = matches[-6:-1]   # 1–5
    curr_5 = matches[-5:]    # 2–6

    def calc_points(match_list):
        pts = 0
        for m in match_list:
            if m.home_team == team:
                gf, ga = m.home_goals, m.away_goals
            else:
                gf, ga = m.away_goals, m.home_goals

            if gf > ga:
                pts += 3
            elif gf == ga:
                pts += 1
        return pts

    prev_points = calc_points(prev_5)
    curr_points = calc_points(curr_5)

    if curr_points > prev_points:
        return 1
    elif curr_points < prev_points:
        return -1
    return 0


def get_team_standings(season, team):

    matches = Match.objects.filter(is_finished=True, season=season).filter(
        Q(home_team=team) | Q(away_team=team)
    )

    pl = matches.count()
    wn = dr = ls = gf = ga = pn = 0

    for match in matches:
        if match.home_team == team:
            goals_for = match.home_goals
            goals_against = match.away_goals
        else:
            goals_for = match.away_goals
            goals_against = match.home_goals

        gf += goals_for
        ga += goals_against

        if goals_for > goals_against:
            wn, pn = wn + 1, pn + 3
        elif goals_for == goals_against:
            dr, pn = dr + 1, pn + 1
        else:
            ls += 1

    return {
        "team": team,
        "played": pl,
        "wins": wn,
        "draws": dr,
        "losses": ls,
        "goals_for": gf,
        "goals_against": ga,
        "goal_difference": gf - ga,
        "points": pn,
        "last_5": get_last_5_results(season, team),
        "form_trend": get_form_trend(season, team),
    }

def get_all_standings(season):

    if not season:
        return []

    teams = Team.objects.filter(Q(home_matches__season=season) | Q(away_matches__season=season)).distinct()

    table = []

    for team in teams:
        row = get_team_standings(season, team)
        table.append(row)

    return sorted(
        table,
        key=lambda x: (
            -x["points"],
            -x["goal_difference"],
            -x["goals_for"],
            x["goals_against"],
        )
    )