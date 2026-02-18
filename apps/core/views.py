from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.users.models import CustomUser
from django.contrib import messages
from apps.news.models import News
from . import utils
from apps.matches.utils import get_matches
from apps.leagues.models import Season, TeamType
from .models import Contact, Message, Video
from django.utils import timezone
from datetime import timedelta

def index(request):

    news_list = News.objects.filter(is_published=True).select_related('category').order_by('-created_at')

    news_prev_2 = news_list[1:3]
    news_prev_3 = news_list[3:6]

    season = Season.objects.order_by('-year').first()

    next_matches = []
    finish_matchs = []

    team_types = TeamType.objects.order_by('order')

    for team in team_types:
        next_match = get_matches(season, team_type=team.code, finished=False, order='first', single=True)
        finish_match = get_matches(season, team_type=team.code, finished=True, order='last', single=True)

        next_matches.append({'team_type': team.name.split()[0], 'code': team.code, 'match': next_match})
        finish_matchs.append({'team_type': team.name.split()[0], 'code': team.code, 'match': finish_match})

    videos = Video.objects.filter(is_active=True).order_by('-created_at')[:3]

    context = {
        'news': news_list[:3],
        'news_prev_2': news_prev_2,
        'news_prev_3': news_prev_3,
        'next_matches': next_matches,
        'finish_matches': finish_matchs,
        'videos': videos
    }
    context.update(utils.get_base_context(request))
    return render(request, 'core/index.html', context)

def contacts(request):

    contact = Contact.objects.all().first()

    if request.method == 'POST':

        if not request.user.is_authenticated:
            messages.error(request, "Xabar yozish uchun tizimga kiring yoki ro'yxatdan o'ting")
            return redirect('contacts')
        
        full_name=request.POST.get('full_name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        message=request.POST.get('message')

        if not all([full_name, email, phone, message]):
            messages.error(request, "Iltimos barcha maydonlarni to'ldiring")
            return redirect('contacts')
        
        last_message = Message.objects.filter(
            user=request.user
        ).order_by('-created_at').first()

        if last_message:
            time_diff = timezone.now() - last_message.created_at
            if time_diff < timedelta(hours=24):
                remaining_time = timedelta(hours=24) - time_diff
                hours = remaining_time.seconds // 3600

                messages.error(request, f"Siz xabarni faqat {hours} soatdan keyin qayta yubora olasiz")
                return redirect('contacts')
        
        Message.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            message=message,
            user=request.user
        )

        messages.success(request, "Sizning xabaringiz yuborildi")
        return redirect('contacts')

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'contacts', 'url': 'contacts', 'args': []},
    ]
    context = {
        'contact': contact,
        'page_title': 'Bog\'lanish',
        'paths': paths
    }
    context.update(utils.get_base_context(request))

    return render(request, 'core/contacts/contact.html', context)

def sign_in(request):
     
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password').strip()
        rememberme = request.POST.get('rememberme')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Tizimga muvaffaqiyatli kirdingiz')
            
            # Sessiya muddati
            if rememberme:
                request.session.set_expiry(7200)  # 2 soat
            else:
                request.session.set_expiry(1800)  # 30 daqiqa
            
            return redirect('home')
        
        messages.error(request, 'Login yoki parol xato')
        return redirect('sign-in')
        
    context = {
        'page_title': 'Tizimga kirish'
    }
    context.update(utils.get_base_context(request))
    return render(request, 'core/auth/sign-in.html', context)

def sign_up(request):

    if request.method == 'POST':
        
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()

        if not username or not email or not password:
            messages.error(request, "Iltimos barcha maydonlarni to'ldiring.")
            return redirect('sign-up')
        
        if not utils.is_strong_password(password):
            messages.error(request, "Parol murakkab emas")
            return redirect('sign-up')
        
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud.")
            return redirect('sign-up')
        
        user = CustomUser(username=username, email=email)
        user.set_password(password)
        user.save()

        messages.success(request, "Ro'yxatdan o'tish muoffaqiyatli amalga oshirildi")
        return redirect('sign-in')
    
    context = {
        'page_title': 'Ro\'yxatdan o\'tish'
    }
    context.update(utils.get_base_context(request))
    return render(request, 'core/auth/sign-up.html', context)

def sign_out(request):
    logout(request)
    messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz')
    return redirect('home')


from apps.core.utils import get_base_context, paginate_queryset

def galery_video(request):

    videos = Video.objects.all().order_by('-created_at')
    videos, pagination_range = paginate_queryset(videos, request, per_page=9)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'video', 'url': 'galery_video', 'args': []},
    ]

    context = {
        'pagination_range': pagination_range,
        "videos": videos,
        'page_title': 'Vedio lavhalar',
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'core/galery/video.html', context)


def galery_photo(request):

    photos = News.objects.all().order_by('-created_at')
    photos, pagination_range = paginate_queryset(photos, request, per_page=9)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'photo', 'url': 'galery_photo', 'args': []},
    ]

    context = {
        'pagination_range': pagination_range,
        "photos": photos,
        'page_title': 'Foto lavhalar',
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'core/galery/photo.html', context)