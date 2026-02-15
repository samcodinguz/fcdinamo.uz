from django.shortcuts import render
from apps.core.utils import get_base_context, paginate_queryset
from .models import MediaVideo

def media_vedio(request):

    vedios = MediaVideo.objects.all().order_by('-created_at')
    vedios, pagination_range = paginate_queryset(vedios, request, per_page=9)

    paths = [
        {'title': 'home', 'url': 'home', 'args': []},
        {'title': 'media', 'url': 'media_vedios', 'args': []},
        {'title': 'vedio', 'url': 'media_vedios', 'args': []},
    ]

    context = {
        'pagination_range': pagination_range,
        "vedios": vedios,
        'page_title': 'Barcha yangiliklar',
        'paths': paths
    }
    context.update(get_base_context(request))
    return render(request, 'media/vedio.html', context)