from collections import OrderedDict
from apps.teams.models import Coach, PlayerPosition

def group_players_by_position(players, team_type_obj):

    grouped = OrderedDict()
    positions = PlayerPosition.objects.all().order_by('order')

    for position in positions:
        filtered = players.filter(position=position).order_by('order')

        if filtered.exists():
            grouped[position.title] = filtered

    coaches = Coach.objects.filter(team_type=team_type_obj).order_by('order')
    if coaches.exists():
        grouped["Murabbiylar"] = coaches
    return grouped
