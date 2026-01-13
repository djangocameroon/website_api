from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from apps.events.models import Event
from services import NotificationService
from services.notification_preferences import get_notification_preferences

User = get_user_model()


class Command(BaseCommand):
    help = 'Send monthly digest of upcoming events to all users'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Include events for the next N days (default: 30)'
        )
        parser.add_argument(
            '--send-sms',
            action='store_true',
            help='Send SMS digest in addition to email (requires phone_number on user)'
        )

    def handle(self, *args, **options):
        days = options['days']
        prefs = get_notification_preferences()
        send_sms = bool(options.get('send_sms')) or prefs.send_upcoming_digest_sms
        send_email = prefs.send_upcoming_digest_email

        if not (send_sms or send_email):
            return

        # Get upcoming events for the next month
        end_date = now() + timedelta(days=days)
        upcoming_events = Event.objects.filter(
            published=True,
            date__gte=now(),
            date__lte=end_date
        ).order_by('date')

        if not upcoming_events.exists():
            self.stdout.write(
                self.style.WARNING(f'No upcoming events found for the next {days} days')
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'Found {upcoming_events.count()} upcoming events')
        )

        # Get all active users
        users = User.objects.filter(is_active=True)

        self.stdout.write(
            f'Sending digest to {users.count()} active users...'
        )

        notification_service = NotificationService()

        # Send digest to users in batches to avoid overwhelming the email server
        batch_size = 50
        total_sent = 0

        for i in range(0, users.count(), batch_size):
            batch = users[i:i + batch_size]
            for user in batch:
                try:
                    notification_service.send_upcoming_events_digest(
                        [user],
                        list(upcoming_events),
                        send_sms=send_sms,
                        send_email=send_email,
                    )
                    total_sent += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'Error sending to {user.email}: {str(e)}')
                    )

            self.stdout.write(f'Sent {total_sent}/{users.count()} digests...')

        self.stdout.write(
            self.style.SUCCESS(f'✓ Successfully sent {total_sent} event digests!')
        )
