from collections import OrderedDict
from .models import Coach

def group_players_by_position(players, team_type='men'):

    POSITION_LABELS = OrderedDict([
        (0, "Darvozabonlar"),
        (1, "Himoyachilar"),
        (2, "Yarim himoyachilar"),
        (3, "Hujumchilar"),
    ])

    grouped = OrderedDict()

    for order, label in POSITION_LABELS.items():
        print(label)
        filtered = players.filter(
            position__order=order
        ).order_by('order')

        if filtered.exists():
            grouped[label] = filtered

    coaches = Coach.objects.filter(team_type=team_type).order_by('order')
    if coaches.exists():
        grouped["Murabbiylar"] = coaches
    return grouped
