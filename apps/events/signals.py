from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from apps.events.models import Event, EventRegistration
from apps.events.tasks import (
    notify_users_on_event_cancelled_task,
    notify_users_on_new_event_task,
    send_registration_confirmation_task,
)

User = get_user_model()


@receiver(post_save, sender=Event)
def notify_users_on_new_event(sender, instance, created, **kwargs):
    """
    Send notification to all users when a new event is published
    """
    if created and instance.published:
        notify_users_on_new_event_task.delay(instance.pk)


@receiver(pre_save, sender=Event)
def detect_event_cancellation(sender, instance, **kwargs):
    """
    Detect when an event is being cancelled and notify registered users
    """
    if instance.pk:  # Event already exists
        try:
            old_event = Event.objects.get(pk=instance.pk)
            if old_event.published and not instance.published:
                notify_users_on_event_cancelled_task.delay(
                    instance.pk,
                    cancellation_reason="The event has been cancelled by the organizers.",
                    reschedule_info=None,
                )
        except Event.DoesNotExist:
            pass


@receiver(post_save, sender=EventRegistration)
def send_registration_confirmation(sender, instance, created, **kwargs):
    """
    Send confirmation email/SMS when user registers for an event
    """
    if created and not instance.confirmation_sent:
        send_registration_confirmation_task.delay(instance.pk)


@receiver(post_save, sender=EventRegistration)
def update_event_stats(sender, instance, **kwargs):
    """
    Update event attendance statistics when registration changes
    """
    from apps.events.models import EventAttendanceStats

    stats, created = EventAttendanceStats.objects.get_or_create(event=instance.event)
    stats.update_stats()
