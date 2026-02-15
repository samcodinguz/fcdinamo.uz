from datetime import datetime
from apps.leagues.models import TeamType
from apps.core.models import Message

def get_base_context(request):
    unread_messages = 0

    if request.user.is_authenticated and request.user.is_superuser:
        unread_messages = Message.objects.filter(is_read=False).count()
    return {
        'current_year': datetime.now().year,
        'categorys': TeamType.objects.all().order_by('order'),
        'unread_messages': unread_messages,
    }