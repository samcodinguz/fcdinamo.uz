from django.shortcuts import render, redirect, get_object_or_404
from apps.core.utils import get_base_context
from apps.news.models import News, NewsTag
from apps.core.utils import paginate_queryset
from apps.core.models import MyClub
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.models import CustomUser
from django.core.exceptions import PermissionDenied
from apps.teams.models import Team, Player, PlayerPosition, Coach, CoachPosition, Management, ManagementPosition
from apps.matches.models import Match
from apps.leagues.models import Season, League, TeamType
from django.db.models.deletion import ProtectedError
from apps.core.models import Contact
import os

@login_required
def judge(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
    ]

    context = {
        'paths': paths,
        'page_title': 'Admin sahifasi'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/judge.html', context)

@login_required
def judge_news(request):

    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        ids = request.POST.getlist("selected_ids")
        news_list = News.objects.filter(id__in=ids)
        for news in news_list:
            if news.image:
                news.image.delete(save=False)
        news_list.delete()
        messages.success(request, f"{len(ids)} ta yangilik o'chirildi")
        return redirect('judge_news')

    category = request.GET.get('category')
    status = request.GET.get('status')
    per_page = request.GET.get('per_page', 10)

    news_list = News.objects.select_related('category').order_by('-created_at')

    if category and category != "all":
        category = int(category)
        news_list = news_list.filter(category__id=category)

    if status and status != "all":
        if status == "true":
            news_list = news_list.filter(is_published=True)
        elif status == "false":
            news_list = news_list.filter(is_published=False)

    news_list, pagination_range = paginate_queryset(news_list, request, per_page=per_page)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'news', 'url': 'judge_news', 'args': []},
    ]

    context = {
        'category': category,
        'status': status,
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        'news_list': news_list,
        'paths': paths,
        'page_title': 'Yangiliklarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/news/news.html', context)

@login_required
def judge_news_delete(request, news_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    news = get_object_or_404(News, id=news_id)
    if news.image:
        news.image.delete(save=False)
    news.delete()
    messages.success(request, "Yangilik muvaffaqiyatli o'chirildi")
    return redirect('judge_news')

@login_required
def judge_news_edit(request, news_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    news = get_object_or_404(News, id=news_id)

    if request.method == "POST":

        title = request.POST.get('title')
        
        news.title = title if title else news.title
        news.content = request.POST.get('content')
        news.category_id = request.POST.get('category')
        news.author_id = request.POST.get('author')
        news.telegram_url = request.POST.get('telegram_url')
        news.facebook_url = request.POST.get('facebook_url')
        news.instagram_url = request.POST.get('instagram_url')
        news.is_published = request.POST.get('is_published') == 'true'
        tag_ids = request.POST.getlist('tags')
        news.tags.set(tag_ids)

        if 'file' in request.FILES:
            if news.image:
                news.image.delete(save=False)
            news.image = request.FILES['file']

        news.save()
        messages.success(request, "Yangilik muvaffaqiyatli saqlandi")

        return redirect('judge_news')

    categories = TeamType.objects.all()
    users = CustomUser.objects.all()
    tags = NewsTag.objects.all()

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'news', 'url': 'judge_news', 'args': []},
        {'title': 'edit', 'url': 'judge_news_edit', 'args': [news_id]},
        {'title': news_id, 'url': 'judge_news_edit', 'args': [news_id]},
    ]

    context = {
        'news': news,
        "categories": categories,
        "users": users,
        "tags": tags,
        'paths': paths,
        'page_title': 'Yangiliklarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/news/edit.html', context)

@login_required
def judge_news_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category')
        author_id = request.POST.get('author')
        telegram_url = request.POST.get('telegram_url')
        facebook_url = request.POST.get('facebook_url')
        instagram_url = request.POST.get('instagram_url')
        is_published = request.POST.get('is_published') == 'true'
        image = request.FILES.get('file')
        tags = request.POST.getlist('tags')
  
        if not title or not category_id:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_news_add')
        
        category = get_object_or_404(TeamType, id=category_id)
        author = get_object_or_404(CustomUser, id=author_id)

        news = News.objects.create(
            title=title,
            content=content,
            category=category,
            author=author,
            telegram_url=telegram_url,
            facebook_url=facebook_url,
            instagram_url=instagram_url,
            is_published=is_published,
            image=image
        )

        if tags:
            news.tags.set(tags)

        messages.success(request, "Yangilik muvaffaqiyatli yaratildi")
        return redirect('judge_news')

    categories = TeamType.objects.all().order_by('order')
    users = CustomUser.objects.all()
    tags = NewsTag.objects.all()

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'news', 'url': 'judge_news', 'args': []},
        {'title': 'add', 'url': 'judge_news_add', 'args': []},
    ]

    context = {
        "categories": categories,
        "users": users,
        "tags": tags,
        'paths': paths,
        'page_title': 'Yangilik qo\'shish'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/news/add.html', context)




@login_required
def judge_leagues(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        try:
            ids = request.POST.getlist("selected_ids")
            leagues_list = League.objects.filter(id__in=ids)
            leagues_list.delete()
            messages.success(request, f"{len(ids)} ta lega o'chirildi")
        except ProtectedError:
            messages.error(request, "Kategoriyalar orasida ishlatilayotgani bor, o'chirish taqiqlanadi")
        
        return redirect('judge_leagues')

    per_page = request.GET.get('per_page', 10)

    leagues_list = League.objects.all().order_by('-id')
    leagues_list, pagination_range = paginate_queryset(leagues_list, request, per_page=per_page)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'leagues', 'url': 'judge_leagues', 'args': []},
    ]

    context = {
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        "leagues_list": leagues_list,
        'paths': paths,
        'page_title': 'Legalarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/seasons/leagues.html', context)

@login_required
def judge_leagues_delete(request, league_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    try:
        league = get_object_or_404(League, id=league_id)
        league.delete()
        messages.success(request, "Lega muvaffaqiyatli o'chirildi")
    except ProtectedError:
            messages.error(request, "Bu kategoriya ishlatilmoqda, o'chirish taqiqlanadi")

    return redirect('judge_leagues')

@login_required
def judge_leagues_edit(request, league_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    leagues = get_object_or_404(League, id=league_id)

    if request.method == "POST":

        leagues.name = request.POST.get('league_name')
        leagues.save()
        messages.success(request, "Lega muvaffaqiyatli saqlandi")

    return redirect('judge_leagues')

@login_required
def judge_leagues_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        league_name = request.POST.get('league_name')
        
        if not league_name:
            messages.error(request, "Lega nomi kiritilmadi")
            return redirect('judge_leagues')

        League.objects.create(name=league_name)

        messages.success(request, "Lega muvaffaqiyatli yaratildi")
    
    return redirect('judge_leagues')




@login_required
def judge_seasons(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        try:
            ids = request.POST.getlist("selected_ids")
            seasons_list = Season.objects.filter(id__in=ids)
            seasons_list.delete()
            messages.success(request, f"{len(ids)} ta mavsum o'chirildi")
        except ProtectedError:
            messages.error(request, "Mavsumlar orasida ishlatilayotgani bor, o'chirish taqiqlanadi")
        
        return redirect('judge_seasons')

    per_page = request.GET.get('per_page', 10)

    seasons_list = Season.objects.all().order_by('-year', '-id')
    seasons_list, pagination_range = paginate_queryset(seasons_list, request, per_page=per_page)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'seasons', 'url': 'judge_seasons', 'args': []},
    ]

    context = {
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        "seasons_list": seasons_list,
        "leagues": League.objects.all(),
        "team_types": TeamType.objects.all(),
        'paths': paths,
        'page_title': 'Mavsumlarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/seasons/seasons.html', context)

@login_required
def judge_seasons_delete(request, season_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    try:
        season = get_object_or_404(Season, id=season_id)
        season.delete()
        messages.success(request, "Mavsum muvaffaqiyatli o'chirildi")
    except ProtectedError:
            messages.error(request, "Bu mavsum ishlatilmoqda, o'chirish taqiqlanadi")
    
    return redirect('judge_seasons')

@login_required
def judge_seasons_edit(request, season_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    season = get_object_or_404(Season, id=season_id)

    if request.method == "POST":
        
        league_id = request.POST.get("league")
        year = request.POST.get("year")
        team_type_id = request.POST.get("team_type")
        is_active = request.POST.get("is_active") == "on"
        
        if not league_id or not year or not team_type_id:
            messages.success(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_seasons')
        
        season.league_id = league_id
        season.year = year
        season.team_type_id = team_type_id
        season.is_active = is_active
        season.save()
        messages.success(request, "Mavsum yangilandi")

    return redirect('judge_seasons')

@login_required
def judge_seasons_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        league_id = request.POST.get("league")
        year = request.POST.get("year")
        team_type_id = request.POST.get("team_type")

        if not league_id or not year or not team_type_id:
            messages.success(request, "Mavsum yangilandi")
            return redirect('judge_seasons')
        
        Season.objects.create(league_id=league_id, year=year, team_type_id=team_type_id)

        messages.success(request, "Mavsum muvaffaqiyatli yaratildi")
    
    return redirect('judge_seasons')




@login_required
def judge_news_tags(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        ids = request.POST.getlist("selected_ids")
        tags_list = NewsTag.objects.filter(id__in=ids)
        tags_list.delete()
        messages.success(request, f"{len(ids)} ta teg o'chirildi")
        return redirect('judge_news_tags')

    per_page = request.GET.get('per_page', 10)

    tags_list = NewsTag.objects.all().order_by('-id')
    tags_list, pagination_range = paginate_queryset(tags_list, request, per_page=per_page)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'news', 'url': 'judge_news', 'args': []},
        {'title': 'tags', 'url': 'judge_news_tags', 'args': []},
    ]

    context = {
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        "tags_list": tags_list,
        'paths': paths,
        'page_title': 'Teglarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/news/tags.html', context)

@login_required
def judge_news_tags_delete(request, tags_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    tags = get_object_or_404(NewsTag, id=tags_id)
    tags.delete()
    messages.success(request, "Teg muvaffaqiyatli o'chirildi")
    return redirect('judge_news_tags')

@login_required
def judge_news_tags_edit(request, tags_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    tags = get_object_or_404(NewsTag, id=tags_id)

    if request.method == "POST":

        tags.name = request.POST.get('tag_name')
        tags.save()
        messages.success(request, "Teg muvaffaqiyatli saqlandi")

    return redirect('judge_news_tags') 
    
@login_required
def judge_news_tags_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        tag_name = request.POST.get('tag_name')
        
        if not tag_name:
            messages.error(request, "Teg nomi kiritilmadi")
            return redirect('judge_news_tags')

        NewsTag.objects.create(name=tag_name)

        messages.success(request, "Teg muvaffaqiyatli yaratildi")
    
    return redirect('judge_news_tags')


@login_required
def judge_clubs(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        try:
            ids = request.POST.getlist("selected_ids")
            clubs_list = Team.objects.filter(id__in=ids)
            for clubs in clubs_list:
                if clubs.logo:
                    clubs.logo.delete(save=False)
            clubs_list.delete()
            messages.success(request, f"{len(ids)} ta klub o'chirildi")
        except ProtectedError:
            messages.error(request, "Klublar orasida ishlatilayotgani bor, o'chirish taqiqlanadi")
        return redirect('judge_clubs')
    
    per_page = request.GET.get('per_page', 10)
    clubs_list = Team.objects.all().order_by('-id')

    clubs_list, pagination_range = paginate_queryset(clubs_list, request, per_page=per_page)


    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'matches', 'url': 'judge_clubs', 'args': []},
        {'title': 'clubs', 'url': 'judge_clubs', 'args': []},
    ]

    context = {
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        'clubs_list': clubs_list,
        'paths': paths,
        'page_title': 'Klublarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/matches/clubs.html', context)

@login_required
def judge_clubs_delete(request, clubs_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    clubs = get_object_or_404(Team, id=clubs_id)
    try:
        if clubs.logo:
            clubs.logo.delete(save=False)
        clubs.delete()
        messages.success(request, "Klub muvaffaqiyatli o'chirildi")
    except ProtectedError:
            messages.error(request, "Bu klub ishlatilmoqda, o'chirish taqiqlanadi")
    return redirect('judge_clubs')

@login_required
def judge_clubs_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        name = request.POST.get('name')
        short_name = request.POST.get('short_name')
        logo = request.FILES.get('logo')
        
        if not name or not short_name or not logo:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_clubs')

        Team.objects.create(name=name, short_name=short_name, logo=logo)
        messages.success(request, "Klub muvaffaqiyatli yaratildi")
    
    return redirect('judge_clubs')

@login_required
def judge_clubs_edit(request, clubs_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    club = get_object_or_404(Team, id=clubs_id)

    if request.method == "POST":
        name = request.POST.get("name")
        short_name = request.POST.get("short_name")

        if not name or not short_name:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect("judge_clubs")
        
        club.name = name
        club.short_name = short_name

        if 'logo' in request.FILES:
            if club.logo:
                club.logo.delete(save=False)
            club.logo = request.FILES.get("logo")

        club.save()
        messages.success(request, "Klub muvaffaqiyatli yangilandi")

    return redirect("judge_clubs")

@login_required
def judge_team_type(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        try:
            ids = request.POST.getlist("selected_ids")
            TeamType.objects.filter(id__in=ids).delete()
            messages.success(request, f"{len(ids)} ta tur o'chirildi")
        except ProtectedError:
            messages.error(request, "Kategoriyalar orasida ishlatilayotgani bor, o'chirish taqiqlanadi")
        return redirect('judge_team_type')
    
    per_page = request.GET.get('per_page', 10)
    team_type_list = TeamType.objects.all().order_by('order')

    team_type_list, pagination_range = paginate_queryset(team_type_list, request, per_page=per_page)


    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'team', 'url': 'judge_team_type', 'args': []},
        {'title': 'type', 'url': 'judge_team_type', 'args': []},
    ]

    context = {
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        'team_type_list': team_type_list,
        'paths': paths,
        'page_title': 'Klub jamoalarini sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/types.html', context)

@login_required
def judge_team_type_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        code = request.POST.get('code').lower().strip()
        name = request.POST.get('name')
        order = request.POST.get('order')
        
        if not code or not name or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_team_type')

        TeamType.objects.create(code=code, name=name, order=order)
        messages.success(request, "Jamoa turi muvaffaqiyatli yaratildi")
    
    return redirect('judge_team_type')

@login_required
def judge_team_type_edit(request, team_type_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    teamtype = get_object_or_404(TeamType, id=team_type_id)

    if request.method == "POST":
        code = request.POST.get("code")
        name = request.POST.get("name")
        order = request.POST.get("order")

        if not code or not name or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect("judge_team_type")
        
        teamtype.code = code
        teamtype.name = name
        teamtype.order = order

        teamtype.save()
        messages.success(request, "Jamoa turi muvaffaqiyatli yangilandi")

    return redirect("judge_team_type")

@login_required
def judge_team_type_delete(request, team_type_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    try:
        team_type = get_object_or_404(TeamType, id=team_type_id)
        team_type.delete()
        messages.success(request, "Jamoa turi muvaffaqiyatli o'chirildi")
    except ProtectedError:
        messages.error(request, "Bu kategoriya ishlatilmoqda, o'chirish taqiqlanadi")
    return redirect('judge_team_type')




@login_required
def judge_matches(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        ids = request.POST.getlist("selected_ids")
        matches_list = Match.objects.filter(id__in=ids)
        matches_list.delete()
        messages.success(request, f"{len(ids)} ta o'yin o'chirildi")
        return redirect('judge_matches')

    per_page = request.GET.get('per_page', 10)
    category = request.GET.get('category')
    season = request.GET.get('season')

    matches_list = Match.objects.select_related(
        'season', 'home_team', 'away_team'
    ).order_by('is_finished', '-match_date')

    seasons_qs = Season.objects.all()

    if category and category != "all":
        category = int(category)
        matches_list = matches_list.filter(season__team_type__id=category)
        seasons_qs = seasons_qs.filter(team_type_id=category)

    seasons_list = (
        seasons_qs
        .values_list('year', flat=True)
        .distinct()
        .order_by('-year')
    )

    if season and season != "all":
        season_int = int(season)
        if season_int not in seasons_list:
            season = None

    if season and season != "all":
        season = int(season)
        matches_list = matches_list.filter(season__year=season)


    matches_list, pagination_range = paginate_queryset(matches_list, request, per_page=per_page)

    leagues = League.objects.all()

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'matches', 'url': 'judge_clubs', 'args': []},
    ]

    context = {
        'category': category,
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        'matches_list': matches_list,
        'teams': Team.objects.all(),
        'leagues':leagues,
        'season': season,
        'seasons': seasons_list,
        'paths': paths,
        'page_title': 'O\'yinlarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/matches/matches.html', context)

@login_required
def judge_matches_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        team_type_id = request.POST.get("team_type")
        league_id = request.POST.get("league")
        season_year = request.POST.get("season_year")
        home_team_id = request.POST.get("home_team")
        away_team_id = request.POST.get("away_team")
        match_date = request.POST.get("match_date")

        home_goals = request.POST.get("home_goals")
        away_goals = request.POST.get("away_goals")
        is_finished = request.POST.get("is_finished") == 'on'

        if home_team_id == away_team_id:
            messages.error(request, "Uy va mehmon jamoa bir xil bo'lishi mumkin emas")
            return redirect("judge_matches")
        
        season = Season.objects.filter(year=season_year, team_type_id=team_type_id, league_id=league_id).first()

        if not season:
            messages.error(request, "Bunday mavsum topilmadi")
            return redirect("judge_matches")
        
        if is_finished:
            Match.objects.create(
                season=season,
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                match_date=match_date,
                home_goals=home_goals,
                away_goals=away_goals,
                is_finished=is_finished
            )
        else:
            Match.objects.create(
                season=season,
                home_team_id=home_team_id,
                away_team_id=away_team_id,
                match_date=match_date
            )

        messages.success(request, "O'yin muvaffaqiyatli qo'shildi")
    
    return redirect("judge_matches")
        
@login_required
def judge_matches_edit(request, match_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    match = get_object_or_404(Match, id=match_id)

    if request.method == "POST":

        home_goals = request.POST.get('home_goals')
        away_goals = request.POST.get('away_goals')
        is_finished = request.POST.get('is_finished') == 'on'

        if home_goals is None or away_goals is None:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_matches')
        
        match.home_goals = home_goals
        match.away_goals = away_goals     
        match.is_finished = is_finished
        match.save()
        messages.success(request, "O'yin muvaffaqiyatli saqlandi")

    return redirect('judge_matches') 

@login_required
def judge_matches_delete(request, match_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    match = get_object_or_404(Match, id=match_id)
    match.delete()
    messages.success(request, "O'yin muvaffaqiyatli o'chirildi")
    return redirect('judge_matches')




@login_required
def judge_players(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        ids = request.POST.getlist("selected_ids")
        players_list = Player.objects.filter(id__in=ids)
        for player in players_list:
            if player.image:
                player.image.delete(save=False)
        players_list.delete()
        messages.success(request, f"{len(ids)} ta o'yinchi o'chirildi")
        return redirect('judge_players')

    per_page = request.GET.get('per_page', 10)
    category = request.GET.get('category')
    position = request.GET.get('position')

    players_list = Player.objects.select_related('position', 'team_type').order_by('-id')
    positions = PlayerPosition.objects.order_by('order')

    if category and category != "all":
        category = int(category)
        players_list = players_list.filter(team_type__id=category)
    
    if position and position != "all":
        position = int(position)
        players_list = players_list.filter(position__id=position)

    players_list, pagination_range = paginate_queryset(players_list, request, per_page=per_page)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'players', 'url': 'judge_players', 'args': []},
    ]

    context = {
        'category': category,
        'position': position,
        'positions': positions,
        'players_list': players_list,
        'pagination_range': pagination_range,
        'per_page': str(per_page),
        'paths': paths,
        'page_title': 'O\'yinchilarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/players/players.html', context)

@login_required
def judge_players_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        name = request.POST.get('name')
        position = request.POST.get('position')
        team_type = request.POST.get('team_type')
        date_of_birth = request.POST.get('date_of_birth')
        location = request.POST.get('location')
        joined_date = request.POST.get('joined_date')
        image = request.FILES.get('image')
        biography = request.POST.get('biography')
        number = request.POST.get('number')
        order = request.POST.get('order')
  
        if not name or not position or not team_type or not date_of_birth or not location or not joined_date or not image or not number or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_players')
        
        team_type = get_object_or_404(TeamType, id=team_type)
        position = get_object_or_404(PlayerPosition, id=position)

        Player.objects.create(
            name=name,
            position=position,
            team_type=team_type,
            date_of_birth=date_of_birth,
            location=location,
            joined_date=joined_date,
            image=image,
            biography=biography,
            number=number,
            order=order
        )

        messages.success(request, "O'yinchi muvaffaqiyatli yaratildi")
        return redirect("judge_players")
    
    categories = TeamType.objects.all().order_by('order')
    positions = PlayerPosition.objects.order_by('order')

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'players', 'url': 'judge_players', 'args': []},
        {'title': 'add', 'url': 'judge_players_add', 'args': []},
    ]

    context = {
        "categories": categories,
        'positions': positions,
        'paths': paths,
        'page_title': 'O\'yinchi qo\'shish'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/players/add.html', context)

@login_required
def judge_players_delete(request, player_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    player = get_object_or_404(Player, id=player_id)
    player.delete()
    messages.success(request, "O'yinchi muvaffaqiyatli o'chirildi")
    return redirect('judge_players')

@login_required
def judge_players_edit(request, player_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    player = get_object_or_404(Player, id=player_id)

    if request.method == "POST":
        player.name = request.POST.get("name")
        player.location = request.POST.get("location")
        player.team_type_id = request.POST.get("team_type")
        player.position_id = request.POST.get("position")
        player.date_of_birth = request.POST.get("date_of_birth")
        player.joined_date = request.POST.get("joined_date")
        player.number = request.POST.get("number")
        player.order = request.POST.get("order")
        player.biography = request.POST.get("biography", "")

        if request.FILES.get("image"):
            if player.image:
                player.image.delete(save=False)
            player.image = request.FILES["image"]

        player.save()
        messages.success(request, "O'yinchi yangilandi")
        return redirect("judge_players")
    
    categories = TeamType.objects.all().order_by('order')
    positions = PlayerPosition.objects.order_by('order')

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'players', 'url': 'judge_players', 'args': []},
        {'title': 'edit', 'url': 'judge_players_edit', 'args': []},
    ]

    context = {
        'player': player,
        "categories": categories,
        'positions': positions,
        'paths': paths,
        'page_title': 'O\'yinchini tahrirlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/players/edit.html', context)



@login_required
def judge_players_position(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        try:
            ids = request.POST.getlist("selected_ids")
            PlayerPosition.objects.filter(id__in=ids).delete()
            messages.success(request, f"{len(ids)} ta lavozim o'chirildi")
        except ProtectedError:
            messages.error(request, "Lavozimlar orasida ishlatilayotgani bor, o'chirish taqiqlanadi")
        return redirect('judge_players_position')
    
    per_page = request.GET.get('per_page', 10)
    player_positions_list = PlayerPosition.objects.all().order_by('order')

    player_positions_list, pagination_range = paginate_queryset(player_positions_list, request, per_page=per_page)


    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'players', 'url': 'judge_players_position', 'args': []},
        {'title': 'position', 'url': 'judge_players_position', 'args': []},
    ]

    context = {
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        'player_positions_list': player_positions_list,
        'paths': paths,
        'page_title': 'O\'yinchi lavozimlarini sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/players/positions.html', context)

@login_required
def judge_players_position_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        title = request.POST.get('title')
        order = request.POST.get('order')
        
        if not title or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_players_position')

        PlayerPosition.objects.create(title=title, order=order)
        messages.success(request, "Lavozim turi muvaffaqiyatli yaratildi")
    
    return redirect('judge_players_position')

@login_required
def judge_players_position_edit(request, position_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    position = get_object_or_404(PlayerPosition, id=position_id)

    if request.method == "POST":
        title = request.POST.get("title")
        order = request.POST.get("order")

        if not title or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect("judge_players_position")
        
        position.title = title
        position.order = order

        position.save()
        messages.success(request, "Lavozim turi muvaffaqiyatli yangilandi")

    return redirect("judge_players_position")

@login_required
def judge_players_position_delete(request, position_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    try:
        position = get_object_or_404(PlayerPosition, id=position_id)
        position.delete()
        messages.success(request, "Lavozim turi muvaffaqiyatli o'chirildi")
    except ProtectedError:
        messages.error(request, "Bu lavozim ishlatilmoqda, o'chirish taqiqlanadi")
    return redirect('judge_players_position')




@login_required
def judge_coachs(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        ids = request.POST.getlist("selected_ids")
        coachs_list = Coach.objects.filter(id__in=ids)
        for coach in coachs_list:
            if coach.image:
                coach.image.delete(save=False)
        coachs_list.delete()
        messages.success(request, f"{len(ids)} ta murabbiy o'chirildi")
        return redirect('judge_coachs')

    per_page = request.GET.get('per_page', 10)
    category = request.GET.get('category')
    position = request.GET.get('position')

    coachs_list = Coach.objects.select_related('position', 'team_type').order_by('-id')
    positions = CoachPosition.objects.order_by('order')

    if category and category != "all":
        category = int(category)
        coachs_list = coachs_list.filter(team_type__id=category)
    
    if position and position != "all":
        position = int(position)
        coachs_list = coachs_list.filter(position__id=position)

    coachs_list, pagination_range = paginate_queryset(coachs_list, request, per_page=per_page)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'coachs', 'url': 'judge_coachs', 'args': []},
    ]

    context = {
        'category': category,
        'position': position,
        'positions': positions,
        'coachs_list': coachs_list,
        'pagination_range': pagination_range,
        'per_page': str(per_page),
        'paths': paths,
        'page_title': 'O\'yinchilarni sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/coachs/coachs.html', context)

@login_required
def judge_coachs_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        name = request.POST.get('name')
        position = request.POST.get('position')
        team_type = request.POST.get('team_type')
        date_of_birth = request.POST.get('date_of_birth')
        location = request.POST.get('location')
        joined_date = request.POST.get('joined_date')
        image = request.FILES.get('image')
        biography = request.POST.get('biography')
        order = request.POST.get('order')
  
        if not name or not position or not team_type or not date_of_birth or not location or not joined_date or not image or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_coachs')
        
        team_type = get_object_or_404(TeamType, id=team_type)
        position = get_object_or_404(CoachPosition, id=position)

        Coach.objects.create(
            name=name,
            position=position,
            team_type=team_type,
            date_of_birth=date_of_birth,
            location=location,
            joined_date=joined_date,
            image=image,
            biography=biography,
            order=order
        )

        messages.success(request, "Murabbiy muvaffaqiyatli yaratildi")
        return redirect("judge_coachs")
    
    categories = TeamType.objects.all().order_by('order')
    positions = CoachPosition.objects.order_by('order')

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'coachs', 'url': 'judge_coachs', 'args': []},
        {'title': 'add', 'url': 'judge_coachs_add', 'args': []},
    ]

    context = {
        "categories": categories,
        'positions': positions,
        'paths': paths,
        'page_title': 'O\'yinchi qo\'shish'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/coachs/add.html', context)

@login_required
def judge_coachs_delete(request, coach_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    coach = get_object_or_404(Coach, id=coach_id)
    coach.delete()
    messages.success(request, "Murabbiy muvaffaqiyatli o'chirildi")
    return redirect('judge_coachs')

@login_required
def judge_coachs_edit(request, coach_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    coach = get_object_or_404(Coach, id=coach_id)

    if request.method == "POST":
        coach.name = request.POST.get("name")
        coach.location = request.POST.get("location")
        coach.team_type_id = request.POST.get("team_type")
        coach.position_id = request.POST.get("position")
        coach.date_of_birth = request.POST.get("date_of_birth")
        coach.joined_date = request.POST.get("joined_date")
        coach.order = request.POST.get("order")
        coach.biography = request.POST.get("biography", "")

        if request.FILES.get("image"):
            if coach.image:
                coach.image.delete(save=False)
            coach.image = request.FILES["image"]

        coach.save()
        messages.success(request, "Murabbiy yangilandi")
        return redirect("judge_coachs")
    
    categories = TeamType.objects.all().order_by('order')
    positions = CoachPosition.objects.order_by('order')

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'coachs', 'url': 'judge_coachs', 'args': []},
        {'title': 'edit', 'url': 'judge_coachs_edit', 'args': []},
    ]

    context = {
        'coach': coach,
        "categories": categories,
        'positions': positions,
        'paths': paths,
        'page_title': f'{coach.name}ni tahrirlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/coachs/edit.html', context)




@login_required
def judge_coachs_position(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        try:
            ids = request.POST.getlist("selected_ids")
            CoachPosition.objects.filter(id__in=ids).delete()
            messages.success(request, f"{len(ids)} ta lavozim o'chirildi")
        except ProtectedError:
            messages.error(request, "Lavozimlar orasida ishlatilayotgani bor, o'chirish taqiqlanadi")
        return redirect('judge_coachs_position')
    
    per_page = request.GET.get('per_page', 10)
    coach_positions_list = CoachPosition.objects.all().order_by('order')

    coach_positions_list, pagination_range = paginate_queryset(coach_positions_list, request, per_page=per_page)


    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'coachs', 'url': 'judge_coachs_position', 'args': []},
        {'title': 'position', 'url': 'judge_coachs_position', 'args': []},
    ]

    context = {
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        'coach_positions_list': coach_positions_list,
        'paths': paths,
        'page_title': 'Murabbiy lavozimlarini sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/coachs/positions.html', context)

@login_required
def judge_coachs_position_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        title = request.POST.get('title')
        order = request.POST.get('order')
        
        if not title or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_coachs_position')

        CoachPosition.objects.create(title=title, order=order)
        messages.success(request, "Lavozim turi muvaffaqiyatli yaratildi")
    
    return redirect('judge_coachs_position')

@login_required
def judge_coachs_position_edit(request, position_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    position = get_object_or_404(CoachPosition, id=position_id)

    if request.method == "POST":
        title = request.POST.get("title")
        order = request.POST.get("order")

        if not title or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect("judge_coachs_position")
        
        position.title = title
        position.order = order

        position.save()
        messages.success(request, "Lavozim turi muvaffaqiyatli yangilandi")

    return redirect("judge_coachs_position")

@login_required
def judge_coachs_position_delete(request, position_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    try:
        position = get_object_or_404(CoachPosition, id=position_id)
        position.delete()
        messages.success(request, "Lavozim turi muvaffaqiyatli o'chirildi")
    except ProtectedError:
        messages.error(request, "Bu lavozim ishlatilmoqda, o'chirish taqiqlanadi")
    return redirect('judge_coachs_position')




@login_required
def judge_managements(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        ids = request.POST.getlist("selected_ids")
        managements_list = Management.objects.filter(id__in=ids)
        for management in managements_list:
            if management.image:
                management.image.delete(save=False)
        managements_list.delete()
        messages.success(request, f"{len(ids)} ta rahbar o'chirildi")
        return redirect('judge_managements')

    per_page = request.GET.get('per_page', 10)

    managements_list = Management.objects.select_related('position').order_by('-id')
    positions = ManagementPosition.objects.order_by('order')

    managements_list, pagination_range = paginate_queryset(managements_list, request, per_page=per_page)

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'managements', 'url': 'judge_managements', 'args': []},
    ]

    context = {
        'positions': positions,
        'managements_list': managements_list,
        'pagination_range': pagination_range,
        'per_page': str(per_page),
        'paths': paths,
        'page_title': 'Rahbariyat xodimlarini sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/managements/managements.html', context)

@login_required
def judge_managements_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":

        name = request.POST.get('name')
        position = request.POST.get('position')
        date_of_birth = request.POST.get('date_of_birth')
        location = request.POST.get('location')
        image = request.FILES.get('image')
        biography = request.POST.get('biography')
        email = request.POST.get('email')
        order = request.POST.get('order')
  
        if not name or not position or not date_of_birth or not location or not image or not order or not email:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_managements')

        position = get_object_or_404(ManagementPosition, id=position)

        Management.objects.create(
            name=name,
            position=position,
            date_of_birth=date_of_birth,
            location=location,
            image=image,
            email=email,
            biography=biography,
            order=order
        )

        messages.success(request, "Rahbar muvaffaqiyatli yaratildi")
        return redirect("judge_managements")
    
    positions = ManagementPosition.objects.order_by('order')

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'managements', 'url': 'judge_managements', 'args': []},
        {'title': 'add', 'url': 'judge_managements_add', 'args': []},
    ]

    context = {
        'positions': positions,
        'paths': paths,
        'page_title': 'Rahbar xodim qo\'shish'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/managements/add.html', context)

@login_required
def judge_managements_delete(request, management_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    management = get_object_or_404(Management, id=management_id)
    management.delete()
    messages.success(request, "Rahbar muvaffaqiyatli o'chirildi")
    return redirect('judge_managements')

@login_required
def judge_managements_edit(request, management_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    management = get_object_or_404(Management, id=management_id)

    if request.method == "POST":
        management.name = request.POST.get("name")
        management.location = request.POST.get("location")
        management.position_id = request.POST.get("position")
        management.date_of_birth = request.POST.get("date_of_birth")
        management.email = request.POST.get("email")
        management.order = request.POST.get("order")
        management.biography = request.POST.get("biography", "")

        if request.FILES.get("image"):
            if management.image:
                management.image.delete(save=False)
            management.image = request.FILES["image"]

        management.save()
        messages.success(request, "Rahbar yangilandi")
        return redirect("judge_managements")
    
    positions = ManagementPosition.objects.order_by('order')

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'managements', 'url': 'judge_managements', 'args': []},
        {'title': 'edit', 'url': 'judge_managements_edit', 'args': []},
    ]

    context = {
        'management': management,
        'positions': positions,
        'paths': paths,
        'page_title': f'{management.name}ni tahrirlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/managements/edit.html', context)




@login_required
def judge_managements_position(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == "POST":
        try:
            ids = request.POST.getlist("selected_ids")
            ManagementPosition.objects.filter(id__in=ids).delete()
            messages.success(request, f"{len(ids)} ta lavozim o'chirildi")
        except ProtectedError:
            messages.error(request, "Lavozimlar orasida ishlatilayotgani bor, o'chirish taqiqlanadi")
        return redirect('judge_managements_position')
    
    per_page = request.GET.get('per_page', 10)
    management_positions_list = ManagementPosition.objects.all().order_by('order')

    management_positions_list, pagination_range = paginate_queryset(management_positions_list, request, per_page=per_page)


    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'managements', 'url': 'judge_managements_position', 'args': []},
        {'title': 'position', 'url': 'judge_managements_position', 'args': []},
    ]

    context = {
        'per_page': str(per_page),
        'pagination_range': pagination_range,
        'management_positions_list': management_positions_list,
        'paths': paths,
        'page_title': 'Rahbar xodimlar lavozimlarini sozlash'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/players/managements/positions.html', context)

@login_required
def judge_managements_position_add(request):
    if not request.user.is_superuser:
        raise PermissionDenied

    if request.method == "POST":
        title = request.POST.get('title')
        order = request.POST.get('order')
        
        if not title or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect('judge_managements_position')

        ManagementPosition.objects.create(title=title, order=order)
        messages.success(request, "Lavozim turi muvaffaqiyatli yaratildi")
    
    return redirect('judge_managements_position')

@login_required
def judge_managements_position_edit(request, position_id):
    if not request.user.is_superuser:
        raise PermissionDenied

    position = get_object_or_404(ManagementPosition, id=position_id)

    if request.method == "POST":
        title = request.POST.get("title")
        order = request.POST.get("order")

        if not title or not order:
            messages.error(request, "Majburiy maydonlar to'ldirilmagan")
            return redirect("judge_managements_position")
        
        position.title = title
        position.order = order

        position.save()
        messages.success(request, "Lavozim turi muvaffaqiyatli yangilandi")

    return redirect("judge_managements_position")

@login_required
def judge_managements_position_delete(request, position_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    try:
        position = get_object_or_404(ManagementPosition, id=position_id)
        position.delete()
        messages.success(request, "Lavozim turi muvaffaqiyatli o'chirildi")
    except ProtectedError:
        messages.error(request, "Bu lavozim ishlatilmoqda, o'chirish taqiqlanadi")
    return redirect('judge_managements_position')




@login_required
def judge_club_infos(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    club = MyClub.objects.select_related('team').first()
    if request.method == "POST":
        
        history = request.POST.get('history')
        achievements = request.POST.get('achievements')
        stadium = request.POST.get('stadium')

        if club:
            club.history = history
            club.achievements = achievements
            club.stadium = stadium
            club.save()
        else:
            MyClub.objects.create(
                history = history,
                achievements = achievements,
                stadium = stadium
            )

        messages.success(request, "Klub ma'lumotlar muvaffaqiyatli yangilandi")
        return redirect('judge_club_infos')


    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'club', 'url': 'judge_club_infos', 'args': []},
        {'title': 'infos', 'url': 'judge_club_infos', 'args': []},
    ]

    context = {
        'club': club,
        'paths': paths,
        'page_title': 'Klub ma\'lumotlari'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/club/club.html', context)


@login_required
def judge_contacts(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    if request.method == 'POST':
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')

        Contact.objects.create(
            phone=phone,
            email=email,
            address=address
        )
        messages.success(request, "Aloqa ma'lumotlari muvaffaqiyatli yangilandi")
        return redirect('judge_contacts')
    

    paths = [
        {'title': 'judge', 'url': 'judge', 'args': []},
        {'title': 'contacts', 'url': 'judge_contacts', 'args': []},
    ]

    context = {
        'paths': paths,
        'page_title': 'Aloqa ma\'lumotlari'
    }
    context.update(get_base_context(request))
    return render(request, 'judge/contacts/contact.html', context)
