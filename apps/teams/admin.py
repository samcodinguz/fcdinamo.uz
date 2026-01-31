from django.contrib import admin
from .models import Team, Management, ManagementPosition, Coach, CoachPosition, PlayerPosition, MenPlayer, WomenPlayer

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')
    search_fields = ('name', 'short_name')

@admin.register(ManagementPosition)
class ManagementPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order',)

@admin.register(Management)
class ManagementAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'date_of_birth', 'location', 'phone', 'email', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'location', 'phone', 'email', 'position__title')
    ordering = ('order',)

@admin.register(CoachPosition)
class CoachPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'date_of_birth', 'location', 'joined_date', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'location', 'position__title')
    ordering = ('order',)

@admin.register(PlayerPosition)
class PlayerPositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    ordering = ('order',)


@admin.register(MenPlayer)
class MenPlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'number', 'date_of_birth', 'location', 'joined_date', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'number')
    ordering = ('order', 'number')


@admin.register(WomenPlayer)
class WomenPlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'number', 'date_of_birth', 'location', 'joined_date', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'number')
    ordering = ('order',)
