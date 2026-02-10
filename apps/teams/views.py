from django.shortcuts import render, redirect, get_object_or_404
from apps.core.utils import get_base_context
from apps.leagues.models import TeamType
from apps.teams.models import Management, ManagementPosition
from apps.teams.models import Coach, CoachPosition
from apps.teams.models import Player, PlayerPosition
from apps.teams.utils import group_players_by_position
from collections import OrderedDict

def managements(request):

    grouped = OrderedDict()
    managements = Management.objects.filter().order_by('order')
    grouped['Raxbariyat'] = managements

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'teams', 'url': 'managements', 'args': []},
        {'title': 'managements', 'url': 'managements', 'args': []},
    ]
    context = {
        'groups': grouped,
        'page_title': 'Raxbariyat jamoasi',
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'teams/managements.html', context)

def coaches(request):
    
    grouped = OrderedDict()
    coaches = Coach.objects.all().order_by('order')

    grouped['Murabbiylar'] = coaches

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'teams', 'url': 'coaches', 'args': []},
        {'title': 'coaches', 'url': 'coaches', 'args': []},
    ]
    context = {
        'groups': grouped,
        'page_title': 'Murabbiylar jamoasi',
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'teams/coaches.html', context)

def players(request, team_type):
    team_type_obj = TeamType.objects.get(code=team_type)
    players = Player.objects.filter(team_type=team_type_obj).select_related('position', 'team_type').order_by('order')

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'players', 'url': 'players', 'args': [team_type]},
        {'title': team_type, 'url': 'players', 'args': [team_type]},
    ]
    context = {
        'groups': group_players_by_position(players, team_type_obj),
        'page_title': f'{team_type_obj.name} jamoasi',
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'teams/players.html', context)

def management_detail(request, id):

    mg_detail = get_object_or_404(Management, id=id)
    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'managements', 'url': 'managements', 'args': []},
        {'title': id, 'url': 'management_detail', 'args': [id]},
    ]
    context = {
        'detail': mg_detail,
        'page_title': mg_detail.name,
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'teams/detail.html', context)

def coach_detail(request, id):

    co_detail = get_object_or_404(Coach, id=id)
    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'coaches', 'url': 'coaches', 'args': []},
        {'title': id, 'url': 'coach_detail', 'args': [id]},
    ]
    context = {
        'detail': co_detail,
        'page_title': co_detail.name,
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'teams/detail.html', context)

def players_detail(request, team_type, player_id):

    teamtype = get_object_or_404(TeamType, code=team_type)
    detail = get_object_or_404(Player, team_type=teamtype, id=player_id)

    grouped = OrderedDict()
    menplayers = Player.objects.filter(position=detail.position).exclude(pk=player_id).select_related('team_type' ,'position').order_by('?')[:4]
    grouped[detail.position] = menplayers
    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'players', 'url': 'players', 'args': [team_type]},
        {'title': team_type, 'url': 'players', 'args': [team_type]},
        {'title': player_id, 'url': 'players_detail', 'args': [team_type, player_id]},
    ]
    context = {
        'groups': grouped,
        'detail': detail,
        'page_title': detail.name,
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'teams/detail.html', context)