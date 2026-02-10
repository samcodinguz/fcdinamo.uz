from django.db import models
from apps.teams.models import Team

class MyClub(models.Model):
    
    team = models.OneToOneField(Team, on_delete=models.PROTECT, blank=True, null=True)

    history = models.TextField(blank=True, null=True)
    achievements = models.TextField(blank=True, null=True)
    stadium = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "MyClub"
        verbose_name_plural = "MyClub"

    def __str__(self):
        if self.team:
            return self.team.name
        return "Jamoa tanlanmagan"