from django.core.management.base import BaseCommand
from apps.events.tasks import send_monthly_digest_task


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
        send_sms = bool(options.get('send_sms'))
        send_monthly_digest_task.delay(days=days, send_sms=send_sms)
        self.stdout.write(self.style.SUCCESS('Queued monthly digest notifications via Celery.'))
