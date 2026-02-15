from django.contrib import admin
from .models import MyClub, Contact, Message, Video

admin.site.register(Video)
admin.site.register(MyClub)
admin.site.register(Contact)
admin.site.register(Message)