from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.events.models.constants import SOCIAL_MEDIA_PLATFORMS
from apps.users.models import BaseModel


class Speaker(BaseModel):
    """
    Speaker model
    """
    name = models.CharField(
        max_length=50, verbose_name="Full Name",
        help_text=_("Speaker's full name"),
    )
    photo = models.URLField(
        null=True, blank=True,
        help_text=_("Speaker's photo"), verbose_name=_("Photo URL"),
    )
    bio = models.TextField(
        help_text=_("Speaker's bio"), verbose_name=_("Biography"),
        null=True, blank=True,
    )
    speciality = models.ForeignKey(
        "SpeakerSpeciality", on_delete=models.CASCADE,
        help_text=_("Speaker's speciality"), verbose_name=_("Speciality"),
        null=True, blank=True,
    )
    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.name.lower().replace(" ", "-")
        self.active = True
        super().save(*args, **kwargs)

    class Meta:
        db_table = "speakers"
        verbose_name = _("Speaker")
        verbose_name_plural = _("Speakers")


class SpeakerSpeciality(models.Model):
    """
    Speaker specialities
    """
    name = models.CharField(
        max_length=50, help_text="Name of the speciality",
        verbose_name="Speciality Name",
    )

    class Meta:
        db_table = "speaker_specialities"
        verbose_name = _("Speaker Speciality")
        verbose_name_plural = _("Speaker Specialities")

    def __str__(self):
        return self.name


class SpeakerSocialMedia(BaseModel):
    speaker = models.ForeignKey(
        Speaker, on_delete=models.CASCADE, related_name="social_media",
        verbose_name=_("Speaker"), help_text=_("Speaker's social media"),
    )
    platform = models.CharField(
        max_length=50, choices=SOCIAL_MEDIA_PLATFORMS,
        verbose_name=_("Social Media Platform"), help_text=_("Social media platform"),
    )
    profile_link = models.CharField(
        max_length=100, verbose_name=_("Profile Link"), help_text=_("Social media profile link"),
    )
    active = models.BooleanField(
        default=True, help_text="Is the social media platform active?",
        verbose_name="Is Active",
    )

    class Meta:
        db_table = "speaker_social_media"
        unique_together = ("speaker", "platform")
        verbose_name = _("Speaker Social Media")
        verbose_name_plural = _("Speaker Social Media")
        ordering = ["speaker", "platform"]
