from dataclasses import dataclass


@dataclass(frozen=True)
class NotificationPreferences:
    send_welcome_email: bool
    send_welcome_sms: bool
    send_signup_email: bool
    send_signup_sms: bool
    send_new_event_email: bool
    send_new_event_sms: bool
    send_event_cancelled_email: bool
    send_event_cancelled_sms: bool
    send_event_reminder_email: bool
    send_event_reminder_sms: bool
    send_upcoming_digest_email: bool
    send_upcoming_digest_sms: bool
    send_registration_confirmation_email: bool
    send_registration_confirmation_sms: bool
    send_new_location_login_email: bool
    send_new_location_login_sms: bool


def get_notification_preferences() -> NotificationPreferences:
    base = NotificationPreferences(
        send_welcome_email=True,
        send_welcome_sms=False,
        send_signup_email=False,
        send_signup_sms=False,
        send_new_event_email=True,
        send_new_event_sms=False,
        send_event_cancelled_email=True,
        send_event_cancelled_sms=True,
        send_event_reminder_email=True,
        send_event_reminder_sms=True,
        send_upcoming_digest_email=True,
        send_upcoming_digest_sms=False,
        send_registration_confirmation_email=True,
        send_registration_confirmation_sms=True,
        send_new_location_login_email=True,
        send_new_location_login_sms=True,
    )

    try:
        from django.db.utils import OperationalError, ProgrammingError
        from apps.users.models import NotificationSettings

        obj = NotificationSettings.get_solo()
        if not obj:
            return base

        return NotificationPreferences(
            send_welcome_email=obj.send_welcome_email,
            send_welcome_sms=obj.send_welcome_sms,
            send_signup_email=obj.send_signup_email,
            send_signup_sms=obj.send_signup_sms,
            send_new_event_email=obj.send_new_event_email,
            send_new_event_sms=obj.send_new_event_sms,
            send_event_cancelled_email=obj.send_event_cancelled_email,
            send_event_cancelled_sms=obj.send_event_cancelled_sms,
            send_event_reminder_email=obj.send_event_reminder_email,
            send_event_reminder_sms=obj.send_event_reminder_sms,
            send_upcoming_digest_email=obj.send_upcoming_digest_email,
            send_upcoming_digest_sms=obj.send_upcoming_digest_sms,
            send_registration_confirmation_email=obj.send_registration_confirmation_email,
            send_registration_confirmation_sms=obj.send_registration_confirmation_sms,
            send_new_location_login_email=obj.send_new_location_login_email,
            send_new_location_login_sms=obj.send_new_location_login_sms,
        )
    except (OperationalError, ProgrammingError):
        return base
    except Exception:
        return base