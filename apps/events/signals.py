from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.events.models import Event, EventRegistration
from services import NotificationService
from services.notification_preferences import get_notification_preferences

User = get_user_model()


@receiver(post_save, sender=Event)
def notify_users_on_new_event(sender, instance, created, **kwargs):
    """
    Send notification to all users when a new event is published
    """
    if created and instance.published:
        prefs = get_notification_preferences()
        notification_service = NotificationService()
        users = User.objects.filter(is_active=True)
        notification_service.send_event_notification(
            users,
            instance,
            send_sms=prefs.send_new_event_sms,
            send_email=prefs.send_new_event_email,
        )


@receiver(pre_save, sender=Event)
def detect_event_cancellation(sender, instance, **kwargs):
    """
    Detect when an event is being cancelled and notify registered users
    """
    if instance.pk:  # Event already exists
        try:
            old_event = Event.objects.get(pk=instance.pk)
            if old_event.published and not instance.published:
                prefs = get_notification_preferences()
                notification_service = NotificationService()
                registered_users = User.objects.filter(
                    event_registrations__event=instance,
                    event_registrations__status='registered'
                ).distinct()

                if registered_users.exists():
                    notification_service.send_event_cancelled_notification(
                        registered_users,
                        instance,
                        cancellation_reason="The event has been cancelled by the organizers.",
                        send_sms=prefs.send_event_cancelled_sms,
                        send_email=prefs.send_event_cancelled_email,
                    )
        except Event.DoesNotExist:
            pass


@receiver(post_save, sender=EventRegistration)
def send_registration_confirmation(sender, instance, created, **kwargs):
    """
    Send confirmation email/SMS when user registers for an event
    """
    if created and not instance.confirmation_sent:
        prefs = get_notification_preferences()
        if not (prefs.send_registration_confirmation_email or prefs.send_registration_confirmation_sms):
            return
        notification_service = NotificationService()
        notification_service.send_registration_confirmation(
            instance.user,
            instance.event,
            instance,
            send_sms=prefs.send_registration_confirmation_sms,
            send_email=prefs.send_registration_confirmation_email,
        )
        instance.confirmation_sent = True
        instance.save(update_fields=['confirmation_sent'])


@receiver(post_save, sender=EventRegistration)
def update_event_stats(sender, instance, **kwargs):
    """
    Update event attendance statistics when registration changes
    """
    from apps.events.models import EventAttendanceStats

    stats, created = EventAttendanceStats.objects.get_or_create(event=instance.event)
    stats.update_stats()
