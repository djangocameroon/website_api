from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.events.models.event import Event
from apps.events.models.base import BaseModel


class Reservation(BaseModel):
    for_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("event"),
    )
    # Waiting for a User model
    # user = models.ForeignKey("User", on_delete=models.CASCADE)
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    sex = models.CharField(
        max_length=10,
        choices=(("Male", "Male"), ("Female", "Female")),
        default="Male",
    )
    check_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} -> {self.for_event.title}"
