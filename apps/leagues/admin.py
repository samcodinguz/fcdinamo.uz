from django.contrib import admin
from .models import League, Season

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    search_fields = ('name',)

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('league', 'year', 'team_type', 'is_active')
    list_filter = ('league',)
    search_fields = ('league',)