import logging

from celery import shared_task

from apps.subs.services import SubscriptionVerificationService

logger = logging.getLogger(__name__)


@shared_task
def send_subscription_verification_email_task(email: str) -> None:
    try:
        SubscriptionVerificationService().send_verification_email(email)
    except Exception:
        logger.exception("Error sending subscription verification email to %s", email)
