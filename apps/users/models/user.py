from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.events.models.speaker import AvailableSocialMedia
from apps.users.models import BaseModel
from apps.users.models.user_manager import UserManager


class User(BaseModel, AbstractUser, PermissionsMixin):
    email = models.EmailField(
        _("email address"), unique=True,
        help_text=_("Enter a valid email address"),
        error_messages={
            "unique": _("A user with that email already exists.")
        }
    )
    profile_image = models.URLField(
        default="https://via.placeholder.com/150", verbose_name=_("Profile Image"),
        help_text=_("URL to the user's profile image"),
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("Phone Number"),
        help_text=_("Phone number for SMS notifications (E.164 format, e.g., +237XXXXXXXXX)")
    )
    otp_codes = GenericRelation("users.OtpCode")

    gender = models.CharField(
        max_length=50,
        choices=(
            ("Male", "Male"),
            ("Female", "Female"),
            ("Prefer not to say", "Prefer not to say"),
        ),
        default="Male",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def send_email_otp(self) -> None:
        from apps.users.tasks import send_email_otp_task

        send_email_otp_task.delay(self.pk)
        return None

    class Meta:
        db_table = "users"
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserSocialAccount(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="social_accounts",
        verbose_name=_("User"), help_text=_("The user's social account"),
    )
    platform = models.ForeignKey(
        AvailableSocialMedia, on_delete=models.CASCADE,
        verbose_name=_("Platform"), help_text=_("The social media platform"),
    )
    link = models.URLField()

    def save(self, *args, **kwargs):
        self.active = self.platform.active
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("user", "platform")
        verbose_name = _("User Social Account")
        verbose_name_plural = _("User Social Accounts")
