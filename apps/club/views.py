from django.shortcuts import render
from apps.core import utils
from apps.core.models import MyClub

def club_history(request):

    club = MyClub.objects.select_related('team').first()

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'club', 'url': 'club_history', 'args': []},
        {'title': 'history', 'url': 'club_history', 'args': []},
    ]

    context = {
        'paths': paths,
        'club': club,
        'page_title': 'Klub tarixi'
    }
    context.update(utils.get_base_context(request))
    return render(request, 'club/history.html', context)

def club_achievements(request):

    club = MyClub.objects.select_related('team').first()

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'club', 'url': 'club_achievements', 'args': []},
        {'title': 'achievements', 'url': 'club_achievements', 'args': []},
    ]

    context = {
        'paths': paths,
        'club': club,
        'page_title': 'Klub yutuqlari'
    }
    context.update(utils.get_base_context(request))
    return render(request, 'club/achievements.html', context)

def club_stadium(request):

    club = MyClub.objects.select_related('team').first()

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'club', 'url': 'club_stadium', 'args': []},
        {'title': 'stadium', 'url': 'club_stadium', 'args': []},
    ]

    context = {
        'paths': paths,
        'club': club,
        'page_title': 'Klub stadioni'
    }
    context.update(utils.get_base_context(request))
    return render(request, 'club/stadium.html', context)