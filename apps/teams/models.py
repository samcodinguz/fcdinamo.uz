from django.db import models
from apps.leagues.models import TeamType

class Team(models.Model):

    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    logo = models.FileField(upload_to='teams/', blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class ManagementPosition(models.Model):
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title

class Management(models.Model):
    name = models.CharField(max_length=255)
    position = models.ForeignKey(ManagementPosition, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    image = models.FileField(upload_to='management/', blank=True, null=True)
    biography = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class CoachPosition(models.Model):
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title
    

class Coach(models.Model):
    
    name = models.CharField(max_length=255)
    position = models.ForeignKey(CoachPosition, on_delete=models.PROTECT)

    team_type = models.ForeignKey(TeamType, on_delete=models.PROTECT)

    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    joined_date = models.DateField(blank=True, null=True)
    image = models.FileField(upload_to='coaches/', blank=True, null=True)
    biography = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name
    

class PlayerPosition(models.Model):
    title = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.title

class Player(models.Model):

    name = models.CharField(max_length=255)
    position = models.ForeignKey(PlayerPosition, on_delete=models.PROTECT)

    team_type = models.ForeignKey(TeamType, on_delete=models.PROTECT)
    
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    joined_date = models.DateField(blank=True, null=True)
    
    image = models.FileField(upload_to='players/', blank=True, null=True)
    biography = models.TextField(blank=True)
    number = models.PositiveIntegerField(blank=True, null=True)
    
    order = models.IntegerField(default=0)


    class Meta:
        ordering = ('order',)

    def __str__(self):
        return self.name