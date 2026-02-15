from django.db import models
from apps.teams.models import Team
from apps.users.models import CustomUser

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
    

class Contact(models.Model):
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.phone
    

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.email}"
