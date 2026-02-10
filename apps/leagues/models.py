from django.db import models

class League(models.Model):

    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='league/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class TeamType(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Season(models.Model):

    league = models.ForeignKey(League, on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField()
    team_type = models.ForeignKey(TeamType, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.league.name} {self.year} ({self.team_type.name})"