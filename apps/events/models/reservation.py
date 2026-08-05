from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.events.models import Event
from apps.users.models import BaseModel


class Reservation(BaseModel):
    for_event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="reservations",
        verbose_name=_("event"),
    )
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    check_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} -> {self.for_event.title}"

    def save(self, *args, **kwargs):
        if self.for_event.external_registration_link:
            raise ValidationError({
                "for_event": _("This event uses external registration; reservations cannot be made here."),
            })
        super().save(*args, **kwargs)

    class Meta:
        db_table = "reservations"
        verbose_name = _("Reservation")
        verbose_name_plural = _("Reservations")
        unique_together = ("for_event", "user")
