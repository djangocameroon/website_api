import secrets

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


def generate_verification_token() -> str:
    return secrets.token_urlsafe(32)


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    unsubscribe_token = models.CharField(
        max_length=255, unique=True, default=generate_verification_token
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class SubscriptionVerificationToken(models.Model):
    """A single-use token proving control of `email`, ahead of a Subscriber existing for it."""
    email = models.EmailField()
    token = models.CharField(max_length=255, unique=True, default=generate_verification_token)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "subscription_verification_tokens"
        verbose_name = _("Subscription Verification Token")
        verbose_name_plural = _("Subscription Verification Tokens")

    def __str__(self):
        return f"{self.email} - {self.token}"

    def has_expired(self) -> bool:
        return self.expires_at < now()
