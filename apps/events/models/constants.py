from enum import Enum
from typing import Tuple


class EventCategory(str, Enum):
    """
    Django Cameroon Event Categories
    """

    WORKSHOPS = "Workshops"
    TALKS = "Talks"


class EventType(str, Enum):
    """
    Django Cameroon Event Types
    """

    ONLINE = "Online"
    IN_PERSON = "In-person"
    HYBRID = "Hybrid"


class Community(str, Enum):
    DJANGO_CAMEROON = "Django Cameroon"
    DJANGO_GIRLS_CAMEROON = "Django Girls Cameroon"


class SocialMediaPlatform(str, Enum):
    """
    Known social media platforms. Reference data for AvailableSocialMedia
    admin entry (name choices + default link) - not DB-enforced, so new
    platforms can still be added freely via the admin if needed.
    """

    TWITTER = "Twitter (X)"
    LINKEDIN = "LinkedIn"
    GITHUB = "GitHub"
    INSTAGRAM = "Instagram"
    FACEBOOK = "Facebook"
    YOUTUBE = "YouTube"
    TIKTOK = "TikTok"
    WHATSAPP = "WhatsApp"
    TELEGRAM = "Telegram"


SOCIAL_MEDIA_PLATFORM_LINKS = {
    SocialMediaPlatform.TWITTER: "https://twitter.com",
    SocialMediaPlatform.LINKEDIN: "https://linkedin.com",
    SocialMediaPlatform.GITHUB: "https://github.com",
    SocialMediaPlatform.INSTAGRAM: "https://instagram.com",
    SocialMediaPlatform.FACEBOOK: "https://facebook.com",
    SocialMediaPlatform.YOUTUBE: "https://youtube.com",
    SocialMediaPlatform.TIKTOK: "https://tiktok.com",
    SocialMediaPlatform.WHATSAPP: "https://whatsapp.com",
    SocialMediaPlatform.TELEGRAM: "https://telegram.org",
}


def build_tuple_types(enum_type) -> Tuple:
    return tuple([(item.value, item.value) for item in enum_type])


EVENT_CATEGORIES = build_tuple_types(EventCategory)
EVENT_TYPES = build_tuple_types(EventType)
COMMUNITIES = build_tuple_types(Community)
SOCIAL_MEDIA_PLATFORMS = build_tuple_types(SocialMediaPlatform)
