from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import errors

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('news/', include('apps.news.urls')),
    path('matches/', include('apps.matches.urls')),
    path('standings/', include('apps.standings.urls')),
    path('teams/', include('apps.teams.urls')),
    path('judge/', include('apps.judge.urls')),
    path('club/', include('apps.club.urls')),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = errors.error_400
handler401 = errors.error_401
handler402 = errors.error_402
handler403 = errors.error_403
handler404 = errors.error_404
handler500 = errors.error_500
