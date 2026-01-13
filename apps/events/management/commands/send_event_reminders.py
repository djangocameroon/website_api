from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from apps.events.models import Event, EventRegistration
from services import NotificationService
from services.notification_preferences import get_notification_preferences

User = get_user_model()


class Command(BaseCommand):
    help = 'Send reminders for upcoming events'

    def add_arguments(self, parser):
        parser.add_argument(
            '--hours',
            type=int,
            default=24,
            help='Send reminders for events happening in this many hours (default: 24)'
        )
        parser.add_argument(
            '--send-sms',
            action='store_true',
            help='Send SMS notifications in addition to emails'
        )

    def handle(self, *args, **options):
        hours = options['hours']
        prefs = get_notification_preferences()
        send_sms = bool(options['send_sms']) or prefs.send_event_reminder_sms

        # Calculate time window
        start_time = now() + timedelta(hours=hours - 1)
        end_time = now() + timedelta(hours=hours + 1)

        # Find upcoming events
        upcoming_events = Event.objects.filter(
            published=True,
            date__gte=start_time,
            date__lte=end_time
        )

        self.stdout.write(
            self.style.SUCCESS(f'Found {upcoming_events.count()} events in the next {hours} hours')
        )

        notification_service = NotificationService()

        for event in upcoming_events:
            # Get registered users who haven't received a reminder
            registrations = EventRegistration.objects.filter(
                event=event,
                status='registered',
                reminder_sent=False
            )

            if registrations.exists():
                users = [reg.user for reg in registrations]

                self.stdout.write(
                    f'Sending reminders to {len(users)} users for event: {event.title}'
                )

                # Send reminders
                notification_service.send_event_reminder(
                    users,
                    event,
                    send_sms=send_sms,
                    send_email=prefs.send_event_reminder_email,
                )

                # Mark reminders as sent
                registrations.update(reminder_sent=True)

                self.stdout.write(
                    self.style.SUCCESS(f'✓ Sent {len(users)} reminders for {event.title}')
                )

        self.stdout.write(self.style.SUCCESS('Reminder task completed!'))
