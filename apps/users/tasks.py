import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now

from apps.users.models.login_history import LoginHistory
from services import MailService
from services import NotificationService
from services.notification_preferences import get_notification_preferences

logger = logging.getLogger(__name__)

User = get_user_model()


@shared_task
def send_user_created_notifications_task(user_id: int) -> None:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    prefs = get_notification_preferences()
    notification_service = NotificationService()

    if prefs.send_welcome_email or prefs.send_welcome_sms:
        notification_service.send_welcome_notification(
            user,
            send_sms=prefs.send_welcome_sms,
            send_email=prefs.send_welcome_email,
        )

    if prefs.send_signup_email or prefs.send_signup_sms:
        notification_service.send_signup_registration_notification(
            user,
            send_sms=prefs.send_signup_sms,
            send_email=prefs.send_signup_email,
        )


@shared_task
def send_new_location_login_alert_task(login_history_id: int) -> None:
    try:
        login_record = LoginHistory.objects.select_related('user').get(pk=login_history_id)
    except LoginHistory.DoesNotExist:
        return

    if login_record.notification_sent:
        return

    prefs = get_notification_preferences()
    if not (prefs.send_new_location_login_email or prefs.send_new_location_login_sms):
        return

    country = getattr(login_record, 'country', '')
    city = getattr(login_record, 'city', '')

    location_string = LoginHistory.get_location_string(country, city)
    if not location_string or location_string == "Unknown location":
        location_string = login_record.ip_address

    login_info = {
        'login_time': getattr(login_record, 'created_at', None) or now(),
        'ip_address': login_record.ip_address,
        'location': location_string,
        'device': (login_record.device_type or '').capitalize() if login_record.device_type else None,
        'browser': login_record.browser if login_record.browser and login_record.browser != 'Unknown' else None,
    }

    try:
        NotificationService().send_new_location_login_alert(
            login_record.user,
            login_info,
            send_sms=prefs.send_new_location_login_sms,
            send_email=prefs.send_new_location_login_email,
        )
        login_record.notification_sent = True
        login_record.save(update_fields=['notification_sent'])
    except Exception:
        logger.exception("Error sending new location login alert for LoginHistory id=%s", login_history_id)


@shared_task
def send_email_otp_task(user_id: int) -> None:
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return

    try:
        MailService().send_otp(user)
    except Exception:
        logger.exception("Error sending OTP email to user id=%s", user_id)
