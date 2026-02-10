from django.db import models
from apps.users.models import CustomUser
from apps.leagues.models import TeamType

class NewsTag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class News(models.Model):
    category = models.ForeignKey(TeamType, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)

    short_description = models.TextField()
    content = models.TextField()

    image = models.ImageField(upload_to='news/')

    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    views_count = models.PositiveIntegerField(default=0)

    tags = models.ManyToManyField(NewsTag, blank=True)

    # Ijtimoiy tarmoqlar
    telegram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"

    def __str__(self):
        return self.title

class NewsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user} - {self.news}"

class NewsLike(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} likes {self.news}"