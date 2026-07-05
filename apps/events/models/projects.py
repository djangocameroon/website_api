from django.utils import timezone
from django.db import models, transaction
from django.db.models import F
from django.utils.translation import gettext_lazy as _

from apps.users.models import BaseModel

MAX_FEATURED_PROJECTS = 3


class Project(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_("Title"))
    description = models.TextField(verbose_name=_("Description"))
    tags = models.JSONField(default=list, blank=True, verbose_name=_("Tags"))
    github_link = models.URLField(
        null=True, blank=True, verbose_name=_("GitHub Link"),
        help_text=_("Link to the GitHub repository"),
    )
    demo_link = models.URLField(
        null=True, blank=True, verbose_name=_("Demo Link"),
        help_text=_("Link to live demo")
    )
    thumbnail = models.URLField(
        null=True, blank=True, verbose_name=_("Thumbnail"),
        help_text=_("Project thumbnail image URL")
    )
    published = models.BooleanField(default=False, verbose_name=_("Published"))
    is_featured = models.BooleanField(
        default=False, verbose_name=_("Featured"),
        help_text=_("Mark as featured project (max 3 featured projects)")
    )
    created_at = models.DateTimeField(auto_now_add=False, verbose_name=_("Created At"))

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        with transaction.atomic():
            if self.is_featured:
                featured_count = (
                    Project.objects
                    .select_for_update()
                    .filter(is_featured=True)
                    .exclude(pk=self.pk)
                    .count()
                )
                if featured_count >= MAX_FEATURED_PROJECTS:
                    raise ValueError(
                        f"Maximum of {MAX_FEATURED_PROJECTS} featured projects allowed"
                    )
            if not self.created_at:
                self.created_at = timezone.now()
            if not self.thumbnail:
                self.thumbnail = "https://minio.reckot.com/djcmr-media/dj-cmr.jpg"
            super().save(*args, **kwargs)

    class Meta:
        db_table = "projects"
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        ordering = ["-created_at"]
