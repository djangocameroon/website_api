from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models import BaseModel


class Partner(BaseModel):
    name = models.CharField(
        max_length=255, unique=True,
        help_text=_("The name of the partner"), verbose_name=_("Name")
    )
    logo = models.URLField(
        help_text=_("The logo of the partner"), verbose_name=_("Logo")
    )
    about = models.TextField(
        help_text=_("About the partner"), verbose_name=_("About")
    )
    website = models.URLField(
        help_text=_("The website of the partner"), verbose_name=_("Website")
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Partner")
        verbose_name_plural = _("Partners")