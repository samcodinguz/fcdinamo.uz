from django.db import models
from apps.leagues.models import Season
from apps.teams.models import Team

class Match(models.Model):

    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    home_team = models.ForeignKey(Team, related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(Team, related_name='away_matches', on_delete=models.CASCADE)

    home_goals = models.PositiveSmallIntegerField(default=0)
    away_goals = models.PositiveSmallIntegerField(default=0)

    match_date = models.DateTimeField()
    is_finished = models.BooleanField(default=False)

    def __str__(self):
        if self.is_finished:
            return f"{self.home_team} {self.home_goals} - {self.away_goals} {self.away_team}"
        else:
            return f"{self.home_team} vs {self.away_team}"
        

