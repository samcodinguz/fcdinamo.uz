from django.contrib import admin
from .models import News, NewsTag

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'is_published', 'created_at')
    list_filter = ('category', 'is_published', 'created_at')
    search_fields = ('title', 'short_description', 'content')
    prepopulated_fields = {'title': ('title',)}

@admin.register(NewsTag)
class NewsTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)