from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.models.user import User
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
    # Or we can use a URLField()
    photo = models.ImageField(
        null=True, upload_to="images/speakers"
    )
    # Social part
    twitter = models.CharField(max_length=50, null=True)
    linkedin = models.CharField(max_length=50, null=True)
    # Maybe necessary for the Read More of the event
    description = models.TextField(null=True)
    # To know who created or updated the speaker
    last_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, to_field="id"
    )

    def __str__(self):
        return self.full_name
