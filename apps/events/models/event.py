from django.db import models

from apps.events.models.constants import (
    COMMUNITIES,
    EVENT_CATEGORIES,
    EVENT_TYPES,
    Community,
    EventCategory,
    EventType,
)
from apps.events.models.speaker import Speaker
from apps.events.models.base import BaseModel
from django.utils.translation import gettext_lazy as _

from utils.main import generate_uuid


class Event(BaseModel):
    category = models.CharField(
        max_length=50, choices=EVENT_CATEGORIES, default=EventCategory.WORKSHOPS
    )
    for_community = models.CharField(
        max_length=50, choices=COMMUNITIES, default=Community.DJANGO_CAMEROON
    )
    title = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=100)
    hour = models.TimeField()
    date = models.DateField()
    type = models.CharField(
        max_length=50, choices=EVENT_TYPES, default=EventType.IN_PERSON
    )
    speaker = models.ForeignKey(Speaker, on_delete=models.CASCADE)
    tags = models.ManyToManyField("EventTag", related_name="events", default=None)
    # TODO: Add field for displying who created the event
    # created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class EventTag(models.Model):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=generate_uuid(),
        editable=False,
        help_text=_("Unique identifier for this object."),
    )
    tag = models.CharField(max_length=50)
    color = models.CharField(
        max_length=10
    )  # I add this because a class with only one prop is too ... short

    def __str__(self):
        return self.tag
