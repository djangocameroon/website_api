from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.events.models.event import Event
from apps.events.models.base import BaseModel
from apps.users.models.user import User


class Reservation(BaseModel):
    for_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("event"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} -> {self.for_event.title}"
