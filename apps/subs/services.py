import os
from typing import Optional

from django.utils.timezone import now, timedelta

from apps.subs.models import Subscriber, SubscriptionVerificationToken
from services.mail_service import MailService

TOKEN_VALIDITY = timedelta(hours=24)


class SubscriptionVerificationService:
    """Generates, verifies, and invalidates email verification tokens for subscribers."""

    def __init__(self, site_url: Optional[str] = None):
        if site_url is None:
            site_url = os.getenv("FRONTEND_URL", "http://localhost:5173")
        self.site_url = site_url
        self.mail_service = MailService()

    def generate_token(self, email: str) -> str:
        """Create a new verification token for the email, invalidating any previous ones."""
        self.invalidate_tokens(email)
        token = SubscriptionVerificationToken.objects.create(
            email=email, expires_at=now() + TOKEN_VALIDITY
        )
        return token.token

    def verify_token(self, token: str) -> Optional[str]:
        """Verify a token, invalidate it, create/activate the Subscriber, and return the email."""
        token_obj = SubscriptionVerificationToken.objects.filter(token=token).first()
        if not token_obj:
            return None

        if token_obj.has_expired():
            token_obj.delete()
            return None

        email = token_obj.email
        token_obj.delete()

        subscriber, created = Subscriber.objects.get_or_create(
            email=email, defaults={"is_verified": True}
        )
        if not created and not subscriber.is_verified:
            subscriber.is_verified = True
            subscriber.save(update_fields=["is_verified"])

        return email

    def invalidate_tokens(self, email: str) -> None:
        SubscriptionVerificationToken.objects.filter(email=email).delete()

    def send_verification_email(self, email: str) -> None:
        token = self.generate_token(email)
        verification_url = f"{self.site_url.rstrip('/')}/newsletter-subscription?token={token}"
        self.mail_service.send_subscription_verification_email(email, verification_url)


class SubscriberUnsubscribeService:
    """Unsubscribes a subscriber using their stable, per-subscriber unsubscribe token."""

    def unsubscribe(self, token: str) -> Optional[str]:
        """Delete the subscriber matching `token` and return its email, or None if not found."""
        subscriber = Subscriber.objects.filter(unsubscribe_token=token).first()
        if not subscriber:
            return None

        email = subscriber.email
        subscriber.delete()
        return email
