from django.core.management.base import BaseCommand
from apps.events.tasks import send_event_reminders_task


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
        send_sms = bool(options['send_sms'])
        send_event_reminders_task.delay(hours=hours, send_sms=send_sms)
        self.stdout.write(self.style.SUCCESS('Queued reminder notifications via Celery.'))
