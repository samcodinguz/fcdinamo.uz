from datetime import datetime
from apps.leagues.models import TeamType
from apps.core.models import Message
import re

def extract_iframe_src(text: str) -> str | None:
    match = re.search(r'src=["\'](https://[^"\']+)["\']', text)
    return match.group(1) if match else None

def get_base_context(request):
    unread_messages = 0

    if request.user.is_authenticated and request.user.is_superuser:
        unread_messages = Message.objects.filter(is_read=False).count()
    return {
        'current_year': datetime.now().year,
        'categorys': TeamType.objects.all().order_by('order'),
        'unread_messages': unread_messages,
    }