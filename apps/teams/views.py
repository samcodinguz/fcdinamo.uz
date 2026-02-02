from django.shortcuts import render, redirect, get_object_or_404
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
        'url': 'management'
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
        'url': 'coach' 
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
        'url': 'men'
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
        'url': 'women'
    }
    context.update(get_base_context(request))
    return render(request, 'teams/womens.html', context)

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

def men_detail(request, id):

    mn_detail = get_object_or_404(MenPlayer, id=id)

    grouped = OrderedDict()
    menplayers = MenPlayer.objects.filter(position=mn_detail.position).exclude(pk=id).select_related('position').order_by('?')[:4]
    grouped[mn_detail.position] = menplayers
    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'players', 'url': 'mens', 'args': []},
        {'title': 'mens', 'url': 'mens', 'args': []},
        {'title': id, 'url': 'men_detail', 'args': [id]},
    ]
    context = {
        'groups': grouped,
        'detail': mn_detail,
        'page_title': mn_detail.name,
        'paths': paths,
        'url': 'men'
    }
    context.update(get_base_context(request))
    return render(request, 'teams/detail.html', context)

def women_detail(request, id):

    wn_detail = get_object_or_404(WomenPlayer, id=id)

    grouped = OrderedDict()
    womenplayers = WomenPlayer.objects.filter(position=wn_detail.position).exclude(pk=id).select_related('position').order_by('?')[:4]
    grouped[wn_detail.position] = womenplayers

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'players', 'url': 'womens', 'args': []},
        {'title': 'mens', 'url': 'womens', 'args': []},
        {'title': id, 'url': 'women_detail', 'args': [id]},
    ]
    context = {
        'groups': grouped,
        'detail': wn_detail,
        'page_title': wn_detail.name,
        'paths': paths,
        'url': 'women'
    }
    context.update(get_base_context(request))
    return render(request, 'teams/detail.html', context)