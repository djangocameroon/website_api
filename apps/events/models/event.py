from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.events.models.constants import (
    COMMUNITIES, EVENT_CATEGORIES,
    EVENT_TYPES, Community,
    EventCategory, EventType,
)
from apps.users.models.base_model import BaseModel


class EventRegion(models.Model):
    name = models.CharField(max_length=50)


class EventCity(models.Model):
    name = models.CharField(max_length=50)
    region = models.ForeignKey(EventRegion, on_delete=models.CASCADE)


class EventVenue(models.Model):
    name = models.CharField(max_length=50)
    city = models.ForeignKey(EventCity, on_delete=models.CASCADE)


class Event(BaseModel):
    category = models.CharField(
        max_length=50, choices=EVENT_CATEGORIES,
        default=EventCategory.WORKSHOPS, help_text=_("The category of the event"),
        verbose_name=_("Event category"),
    )
    for_community = models.CharField(
        max_length=50, choices=COMMUNITIES,
        default=Community.DJANGO_CAMEROON, help_text=_("The community the event is for"),
        verbose_name=_("Event community"),
    )
    title = models.CharField(
        max_length=100, help_text=_("The title of the event"),
        verbose_name=_("Event title"),
    )
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(
        verbose_name=_("Event description"),
        help_text=_("The description of the event"),
    )
    location = models.ForeignKey(
        EventVenue, on_delete=models.CASCADE,
        verbose_name=_("Event location"), help_text=_("The location of the event"),
    )
    date = models.DateTimeField(
        verbose_name=_("Event date"), help_text=_("The date of the event"),
    )
    thumbnail = models.URLField(
        null=True, blank=True,
        verbose_name=_("Event thumbnail"), help_text=_("The thumbnail of the event"),
    )
    type = models.CharField(
        max_length=50, choices=EVENT_TYPES,
        default=EventType.IN_PERSON, help_text=_("The type of the event"),
        verbose_name=_("Event type"),
    )
    speakers = models.ManyToManyField(
        'Speaker', related_name="events",
        verbose_name=_("Event speakers"), help_text=_("The speakers at the event"),
    )
    tags = models.ManyToManyField(
        "EventTag", related_name="events", default=None,
        verbose_name=_("Event tags"), help_text=_("The tags for the event"),
    )
    level = models.CharField(
        max_length=50, null=True, blank=True,
    )
    published = models.BooleanField(
        default=False, help_text=_("Whether the event is published"),
        verbose_name=_("Event published"),
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.title.lower().replace(" ", "-")
            original_slug = self.slug
            counter = 1
            while Event.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    class Meta:
        db_table = "events"
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        unique_together = ("title", "date", "location")

class EventTag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "event_tags"
        verbose_name = _("Event tag")
        verbose_name_plural = _("Event tags")
