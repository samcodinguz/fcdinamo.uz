from django.shortcuts import render
from apps.core.utils import get_base_context
from apps.teams.models import Management, ManagementPosition
from apps.teams.models import Coach, CoachPosition
from apps.teams.models import MenPlayer, WomenPlayer, PlayerPosition
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
        'page_title': 'Raxbariyat',
        'paths': paths,
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
        'page_title': 'Murabbiylar',
        'paths': paths,
    }
    context.update(get_base_context(request))
    return render(request, 'teams/coaches.html', context)

def mens(request):

    menplayers = MenPlayer.objects.filter().select_related('position').order_by('order')

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'players', 'url': 'mens', 'args': []},
        {'title': 'mens', 'url': 'mens', 'args': []},
    ]
    context = {
        'groups': group_players_by_position(menplayers, team_type='men'),
        'page_title': 'Erkaklar jamoasi',
        'paths': paths,
    }
    context.update(get_base_context(request))
    return render(request, 'teams/mens.html', context)

def womens(request):

    womenplayers = WomenPlayer.objects.filter().select_related('position').order_by('order')

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'players', 'url': 'womens', 'args': []},
        {'title': 'womens', 'url': 'womens', 'args': []},
    ]
    context = {
        'groups': group_players_by_position(womenplayers, team_type='women'),
        'page_title': 'Ayollar jamoasi',
        'paths': paths,
    }
    context.update(get_base_context(request))
    return render(request, 'teams/womens.html', context)

