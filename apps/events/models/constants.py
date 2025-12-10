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


def build_tuple_types(enum_type) -> Tuple:
    return tuple([(item.value, item.value) for item in enum_type])


EVENT_CATEGORIES = build_tuple_types(EventCategory)
EVENT_TYPES = build_tuple_types(EventType)
COMMUNITIES = build_tuple_types(Community)
