from django.contrib import admin
from .models import Team
from .models import PlayerPosition, Player
from .models import CoachPosition, Coach
from .models import ManagementPosition, Management

admin.site.register(Team)

admin.site.register(PlayerPosition)
admin.site.register(Player)

admin.site.register(CoachPosition)
admin.site.register(Coach)

admin.site.register(ManagementPosition)
admin.site.register(Management)
