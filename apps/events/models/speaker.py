from django.db import models
from django.utils.translation import gettext_lazy as _

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
        null=False, default="https://via.placeholder.com/150",
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


class AvailableSocialMedia(models.Model):
    """
    Available social media platforms
    """
    name = models.CharField(
        max_length=50, help_text="Name of the social media platform",
        verbose_name="Social Media Platform Name",
    )
    link = models.URLField(
        help_text="Link to the social media platform",
        verbose_name="Social Media Platform Link",
    )
    active = models.BooleanField(
        default=True, help_text="Is the social media platform active?",
        verbose_name="Is Active",
    )

    class Meta:
        db_table = "available_social_media"
        verbose_name = _("Available Social Media")
        verbose_name_plural = _("Available Social Media")


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


class SpeakerSocialMedia(BaseModel):
    speaker = models.ForeignKey(
        Speaker, on_delete=models.CASCADE, related_name="social_media",
        verbose_name=_("Speaker"), help_text=_("Speaker's social media"),
    )
    platform = models.ForeignKey(
        AvailableSocialMedia, on_delete=models.CASCADE,
        verbose_name=_("Social Media Platform"),
        help_text=_("Social media platform"),
    )
    handle = models.CharField(
        max_length=50, verbose_name=_("Handle"), help_text=_("Social media handle"),
    )

    def save(self, *args, **kwargs):
        self.active = self.platform.active
        super().save(*args, **kwargs)

    class Meta:
        db_table = "speaker_social_media"
        unique_together = ("speaker", "platform")
        verbose_name = _("Speaker Social Media")
        verbose_name_plural = _("Speaker Social Media")
        ordering = ["speaker", "platform"]
