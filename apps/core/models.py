from django.db import models
from apps.teams.models import Team

class MyClub(models.Model):
    
    team = models.OneToOneField(Team, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "MyClub"
        verbose_name_plural = "MyClub"

    def __str__(self):
        return self.team.name