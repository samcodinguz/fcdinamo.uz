from django.contrib import admin
from apps.leagues.models import Season
from .models import Match

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('season', 'home_team', 'away_team', 'home_goals', 'away_goals', 'match_date', 'is_finished')
    list_filter = ('season', 'is_finished', 'match_date')
    search_fields = ('home_team__name', 'away_team__name')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "season":
            kwargs["queryset"] = Season.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)