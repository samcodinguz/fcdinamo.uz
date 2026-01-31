from django.db import models

class League(models.Model):

    name = models.CharField(max_length=100)
    logo = models.FileField(upload_to='league/', null=True, blank=True)

    def __str__(self):
        return self.name
    
class Season(models.Model):

    TEAM_TYPE_CHOICES = [
        ('men', "Men's Team"),
        ('women', "Women's Team"),
    ]

    league = models.ForeignKey(League, on_delete=models.CASCADE)
    year = models.PositiveSmallIntegerField()

    team_type = models.CharField(
        max_length=10,
        choices=TEAM_TYPE_CHOICES,
        default='men'
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.league.name} {self.year}/{(self.year + 1)%100} ({self.team_type})"
    
    def title(self):
        return f"{self.league.name} {self.year}/{(self.year + 1)%100}"