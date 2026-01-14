import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils.timezone import now, timedelta

from apps.events.models import Event, EventRegistration
from services import NotificationService
from services.notification_preferences import get_notification_preferences

logger = logging.getLogger(__name__)

User = get_user_model()


@shared_task
def notify_users_on_new_event_task(event_id: int) -> None:
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return

    if not getattr(event, 'published', False):
        return

    prefs = get_notification_preferences()
    if not (prefs.send_new_event_email or prefs.send_new_event_sms):
        return

    users = User.objects.filter(is_active=True)
    NotificationService().send_event_notification(
        users,
        event,
        send_sms=prefs.send_new_event_sms,
        send_email=prefs.send_new_event_email,
    )


@shared_task
def notify_users_on_event_cancelled_task(
    event_id: int,
    cancellation_reason: str | None = None,
    reschedule_info: str | None = None,
) -> None:
    try:
        event = Event.objects.get(pk=event_id)
    except Event.DoesNotExist:
        return

    prefs = get_notification_preferences()
    if not (prefs.send_event_cancelled_email or prefs.send_event_cancelled_sms):
        return

    registered_users = User.objects.filter(
        event_registrations__event=event,
        event_registrations__status='registered'
    ).distinct()

    if not registered_users.exists():
        return

    NotificationService().send_event_cancelled_notification(
        registered_users,
        event,
        cancellation_reason=cancellation_reason,
        reschedule_info=reschedule_info,
        send_sms=prefs.send_event_cancelled_sms,
        send_email=prefs.send_event_cancelled_email,
    )


@shared_task
def send_registration_confirmation_task(registration_id: int) -> None:
    try:
        registration = EventRegistration.objects.select_related('user', 'event').get(pk=registration_id)
    except EventRegistration.DoesNotExist:
        return

    if registration.confirmation_sent:
        return

    prefs = get_notification_preferences()
    if not (prefs.send_registration_confirmation_email or prefs.send_registration_confirmation_sms):
        return

    try:
        NotificationService().send_registration_confirmation(
            registration.user,
            registration.event,
            registration,
            send_sms=prefs.send_registration_confirmation_sms,
            send_email=prefs.send_registration_confirmation_email,
        )
        registration.confirmation_sent = True
        registration.save(update_fields=['confirmation_sent'])
    except Exception:
        logger.exception("Error sending registration confirmation for EventRegistration id=%s", registration_id)


@shared_task
def send_event_reminders_task(hours: int = 24, send_sms: bool = False) -> None:
    prefs = get_notification_preferences()
    send_sms_final = bool(send_sms) or prefs.send_event_reminder_sms
    send_email = prefs.send_event_reminder_email

    if not (send_sms_final or send_email):
        return

    start_time = now() + timedelta(hours=hours - 1)
    end_time = now() + timedelta(hours=hours + 1)

    upcoming_events = Event.objects.filter(
        published=True,
        date__gte=start_time,
        date__lte=end_time
    )

    notification_service = NotificationService()

    for event in upcoming_events:
        registrations = EventRegistration.objects.filter(
            event=event,
            status='registered',
            reminder_sent=False
        ).select_related('user')

        if not registrations.exists():
            continue

        users = [reg.user for reg in registrations]

        try:
            notification_service.send_event_reminder(
                users,
                event,
                send_sms=send_sms_final,
                send_email=send_email,
            )
            registrations.update(reminder_sent=True)
        except Exception:
            logger.exception("Error sending reminders for event id=%s", getattr(event, 'id', None))


@shared_task
def send_monthly_digest_task(days: int = 30, send_sms: bool = False) -> None:
    prefs = get_notification_preferences()
    send_sms_final = bool(send_sms) or prefs.send_upcoming_digest_sms
    send_email = prefs.send_upcoming_digest_email

    if not (send_sms_final or send_email):
        return

    end_date = now() + timedelta(days=days)
    upcoming_events = list(
        Event.objects.filter(
            published=True,
            date__gte=now(),
            date__lte=end_date
        ).order_by('date')
    )

    if not upcoming_events:
        return

    users = User.objects.filter(is_active=True).only('id').iterator(chunk_size=200)
    notification_service = NotificationService()

    for user in users:
        try:
            notification_service.send_upcoming_events_digest(
                [user],
                upcoming_events,
                send_sms=send_sms_final,
                send_email=send_email,
            )
        except Exception:
            logger.exception("Error sending monthly digest to user id=%s", getattr(user, 'id', None))
