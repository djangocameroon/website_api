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


@receiver(pre_save, sender=Event)
def detect_event_publish_or_cancel(sender, instance, **kwargs):
    instance._was_published = False
    if instance.pk:
        try:
            old_event = Event.objects.get(pk=instance.pk)
            if old_event.published and not instance.published:
                notify_users_on_event_cancelled_task.delay(
                    instance.pk,
                    cancellation_reason="The event has been cancelled by the organizers.",
                    reschedule_info=None,
                )
            if not old_event.published and instance.published:
                instance._was_published = True
        except Event.DoesNotExist:
            pass


@receiver(post_save, sender=Event)
def notify_users_on_new_event(sender, instance, created, **kwargs):
    if instance.published and (created or getattr(instance, '_was_published', False)):
        notify_users_on_new_event_task.delay(instance.pk)


@receiver(post_save, sender=EventRegistration)
def send_registration_confirmation(sender, instance, created, **kwargs):
    if created and not instance.confirmation_sent:
        send_registration_confirmation_task.delay(instance.pk)


@receiver(post_save, sender=EventRegistration)
def update_event_stats(sender, instance, **kwargs):
    from apps.events.models import EventAttendanceStats

    stats, _ = EventAttendanceStats.objects.get_or_create(event=instance.event)
    stats.update_stats()
