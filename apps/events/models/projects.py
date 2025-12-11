from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models import BaseModel


class Event(BaseModel):
    """
    Event model
    """
    title = models.CharField(max_length=50, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    date = models.DateField(verbose_name=_("Date"))
    maintainers =  models.ManyToManyField(
        "users.User", verbose_name=_("Maintainers"),
        help_text=_("Maintainers of the event"), related_name="maintained_events",
    )
    github_link = models.URLField(
        null=True, blank=True, verbose_name=_("GitHub Link"),
        help_text=_("Link to the GitHub repository"),
    )

    class Meta:
        db_table = "events"
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

# Gallery to be added here later from: https://developers.google.com/photos/library/guides/overview
