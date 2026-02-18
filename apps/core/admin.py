from django.contrib import admin
from .models import MyClub, Contact, Message, Video, Sponsor, ClubSocial

admin.site.register(Video)
admin.site.register(MyClub)
admin.site.register(Contact)
admin.site.register(Message)
admin.site.register(Sponsor)
admin.site.register(ClubSocial)