from django.shortcuts import render, redirect, get_object_or_404
from apps.core.utils import get_base_context
from apps.news.models import News, NewsTag, NewsCategory
from apps.core.utils import paginate_queryset
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.users.models import CustomUser
from django.core.exceptions import PermissionDenied
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

    news_list = News.objects.all().select_related('category').order_by('-created_at')
    categorys = NewsCategory.objects.all()

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
        'categorys': categorys,
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

    categories = NewsCategory.objects.all()
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
        
        category = NewsCategory.objects.get(id=category_id)
        author = CustomUser.objects.get(id=author_id)

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

    categories = NewsCategory.objects.all()
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
