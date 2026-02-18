from datetime import datetime
from apps.leagues.models import TeamType
from apps.core.models import Message
import re
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile


def crop_to_16_9(image_file, quality=90):
    img = Image.open(image_file)
    original_format = img.format  # PNG yoki JPEG

    width, height = img.size
    target_ratio = 16 / 9
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))

    buffer = BytesIO()

    if original_format == "PNG":
        # PNG — shaffoflikni saqlaymiz
        img.save(buffer, format="PNG", optimize=True)
        extension = "png"
    else:
        # JPEG — RGBA bo‘lsa RGB ga o‘tkazamiz
        if img.mode == "RGBA":
            img = img.convert("RGB")

        img.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=True,
            progressive=True
        )
        extension = "jpg"

    return ContentFile(
        buffer.getvalue(),
        name=f"news_16x9.{extension}"
    )

def crop_to_1_1(image_file, quality=90):
    img = Image.open(image_file)
    original_format = img.format  # PNG yoki JPEG

    width, height = img.size
    target_ratio = 1 / 1
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))

    buffer = BytesIO()

    if original_format == "PNG":
        # PNG — shaffoflikni saqlaymiz
        img.save(buffer, format="PNG", optimize=True)
        extension = "png"
    else:
        # JPEG — RGBA bo‘lsa RGB ga o‘tkazamiz
        if img.mode == "RGBA":
            img = img.convert("RGB")

        img.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=True,
            progressive=True
        )
        extension = "jpg"

    return ContentFile(
        buffer.getvalue(),
        name=f"player_1x1.{extension}"
    )

def crop_to_2_1(image_file, quality=90):
    img = Image.open(image_file)
    original_format = img.format  # PNG, JPEG, WEBP, etc

    width, height = img.size
    target_ratio = 2 / 1
    current_ratio = width / height

    if current_ratio > target_ratio:
        new_width = int(height * target_ratio)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / target_ratio)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))

    buffer = BytesIO()

    # 🔹 FORMAT BO‘YICHA SAQLASH
    if original_format == "PNG":
        img.save(buffer, format="PNG", optimize=True)
        extension = "png"

    elif original_format in ("JPG", "JPEG"):
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.save(
            buffer,
            format="JPEG",
            quality=quality,
            optimize=True,
            progressive=True
        )
        extension = "jpg"

    elif original_format == "WEBP":
        img.save(
            buffer,
            format="WEBP",
            quality=quality,
            method=6
        )
        extension = "webp"

    else:
        # ❗ Fallback — noma’lum formatlar uchun
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        img.save(buffer, format="JPEG", quality=quality)
        extension = "jpg"

    return ContentFile(
        buffer.getvalue(),
        name=f"logo_2x1.{extension}"
    )



from urllib.parse import urlparse, parse_qs


def extract_iframe_src(text: str) -> str | None:
    """
    YouTube iframe kodidan xavfsiz embed URL chiqaradi
    """

    # 1️⃣ iframe ichidan src olish
    iframe_match = re.search(
        r'<iframe[^>]+src=["\']([^"\']+)["\']',
        text,
        re.IGNORECASE
    )
    if not iframe_match:
        return None

    src = iframe_match.group(1).strip()

    # 2️⃣ URL parse qilish
    parsed = urlparse(src)
    domain = parsed.netloc.lower()

    # 3️⃣ Faqat YouTube ruxsat
    if not any(d in domain for d in (
        "youtube.com",
        "youtu.be",
        "youtube-nocookie.com",
    )):
        return None

    video_id = None

    # 4️⃣ watch?v=VIDEO_ID
    if "watch" in parsed.path:
        qs = parse_qs(parsed.query)
        video_id = qs.get("v", [None])[0]

    # 5️⃣ youtu.be/VIDEO_ID
    elif "youtu.be" in domain:
        video_id = parsed.path.lstrip("/")

    # 6️⃣ /embed/VIDEO_ID
    elif "/embed/" in parsed.path:
        video_id = parsed.path.split("/embed/")[-1]

    if not video_id:
        return None

    # 7️⃣ ENG TOZA FORMAT
    return f"https://www.youtube-nocookie.com/embed/{video_id}"

def get_base_context(request):
    unread_messages = 0

    if request.user.is_authenticated and request.user.is_superuser:
        unread_messages = Message.objects.filter(is_read=False).count()
    return {
        'current_year': datetime.now().year,
        'categorys': TeamType.objects.all().order_by('order'),
        'unread_messages': unread_messages,
    }