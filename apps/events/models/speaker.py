from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.main import generate_uuid


class Speaker(models.Model):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=generate_uuid(),
        editable=False,
        help_text=_("Unique identifier for this object."),
    )
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(
        null=True, upload_to="images/speakers"
    )  # Or we can use a URLField()
    # Social part
    twitter = models.CharField(max_length=50, null=True)
    linkedin = models.CharField(max_length=50, null=True)
    description = models.TextField(
        null=True
    )  # Maybe necessary for the Read More of the event

    def __str__(self):
        return self.full_name
