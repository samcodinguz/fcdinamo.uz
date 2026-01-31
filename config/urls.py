from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('news/', include('apps.news.urls')),
    path('matches/', include('apps.matches.urls')),
    path('standings/', include('apps.standings.urls')),
    path('teams/', include('apps.teams.urls')),
    path('judge/', include('apps.judge.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
