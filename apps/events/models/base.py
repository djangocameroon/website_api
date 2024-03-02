from django.db import models
from django.utils.translation import gettext_lazy as _

from utils.main import generate_uuid


class BaseModel(models.Model):
    id = models.UUIDField(
        _("id"),
        primary_key=True,
        default=generate_uuid(),
        editable=False,
        help_text=_("Unique identifier for this object."),
    )
    created_at = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
        help_text=_("Date and time when this object was created."),
    )
