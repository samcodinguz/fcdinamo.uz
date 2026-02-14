from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from apps.users.models import CustomUser
from django.contrib import messages
from apps.news.models import News
from . import utils
from apps.matches.utils import get_matches
from apps.leagues.models import Season

def index(request):

    news_list = News.objects.filter(is_published=True).select_related('category').order_by('-created_at')

    news_prev_2 = news_list[1:3]
    news_prev_3 = news_list[3:6]

    season = Season.objects.order_by('-year').first()
    next_men_match = get_matches(season, team_type='men', finished=False, order='first', single=True)
    last_men_match = get_matches(season, team_type='men', finished=True, order='last', single=True)

    context = {
        'news_first': news_list.first(),
        'news_prev_2': news_prev_2,
        'news_prev_3': news_prev_3,
        'next_men_match': next_men_match,
        'last_men_match': last_men_match,
    }
    context.update(utils.get_base_context(request))
    return render(request, 'core/index.html', context)


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