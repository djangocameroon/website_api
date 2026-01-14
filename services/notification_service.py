import logging
from typing import List, Optional
from django.utils.timezone import now
from services.mail_service import MailService
from services.sms_service import SMSService


logger = logging.getLogger(__name__)


class NotificationService:
    """
    Unified notification service for sending both email and SMS notifications
    """

    def __init__(self, site_url: str = "https://djangocameroon.org"):
        self.mail_service = MailService()
        self.sms_service = SMSService()
        self.site_url = site_url

    def send_welcome_notification(self, user, send_sms: bool = False, send_email: bool = True):
        """
        Send welcome notification to new user

        Args:
            user: User object
            send_sms: Whether to send SMS notification (requires phone_number on user)
        """
        if send_email:
            try:
                self.mail_service.send_welcome_email(user, self.site_url)
            except Exception:
                logger.exception("Error sending welcome email to %s", getattr(user, 'email', None))

        if send_sms and hasattr(user, 'phone_number') and user.phone_number:
            try:
                user_name = user.first_name or user.username
                self.sms_service.send_welcome_sms(user.phone_number, user_name)
            except Exception as e:
                logger.exception("Error sending welcome SMS to %s", getattr(user, 'phone_number', None))

    def send_signup_registration_notification(self, user, send_sms: bool = False, send_email: bool = True):
        """Send signup/registration confirmation (email + optional SMS)."""
        if send_email:
            try:
                self.mail_service.send_signup_confirmation_email(user, self.site_url)
            except Exception:
                logger.exception("Error sending signup confirmation email to %s", getattr(user, 'email', None))

        if send_sms and hasattr(user, 'phone_number') and user.phone_number:
            try:
                user_name = user.first_name or user.username
                self.sms_service.send_signup_confirmation_sms(user.phone_number, user_name)
            except Exception:
                logger.exception("Error sending signup confirmation SMS to %s", getattr(user, 'phone_number', None))

    def send_event_notification(self, users: List, event, send_sms: bool = False, send_email: bool = True):
        """
        Send event notification to multiple users

        Args:
            users: List of User objects
            event: Event object
            send_sms: Whether to send SMS notifications
        """
        for user in users:
            if send_email:
                try:
                    self.mail_service.send_event_notification(user, event, self.site_url)
                except Exception:
                    logger.exception("Error sending event notification email to %s", getattr(user, 'email', None))

            if send_sms and hasattr(user, 'phone_number') and user.phone_number:
                try:
                    event_date = event.date.strftime("%b %d, %Y at %I:%M %p")
                    event_location = f"{event.location.name}, {event.location.city.name}"
                    event_url = f"{self.site_url.rstrip('/')}/events/{event.slug}"
                    self.sms_service.send_event_notification_sms(
                        user.phone_number,
                        event.title,
                        event_date,
                        event_location,
                        event_url=event_url,
                    )
                except Exception as e:
                    logger.exception("Error sending event notification SMS to %s", getattr(user, 'phone_number', None))

    def send_event_cancelled_notification(
            self, users: List, event,
            cancellation_reason: Optional[str] = None,
            reschedule_info: Optional[str] = None,
            send_sms: bool = True,
            send_email: bool = True
        ):
        """
        Send event cancellation notification

        Args:
            users: List of registered users
            event: Event object
            cancellation_reason: Reason for cancellation
            reschedule_info: Information about rescheduling
            send_sms: Whether to send SMS notifications (default True for cancellations)
        """
        for user in users:
            if send_email:
                try:
                    self.mail_service.send_event_cancelled(
                        user, event, cancellation_reason, reschedule_info, self.site_url
                    )
                except Exception:
                    logger.exception("Error sending cancellation email to %s", getattr(user, 'email', None))

            if send_sms and hasattr(user, 'phone_number') and user.phone_number:
                try:
                    event_date = event.date.strftime("%b %d, %Y")
                    event_url = f"{self.site_url.rstrip('/')}/events/{event.slug}"
                    self.sms_service.send_event_cancelled_sms(
                        user.phone_number,
                        event.title,
                        event_date,
                        event_url=event_url,
                    )
                except Exception as e:
                    logger.exception("Error sending cancellation SMS to %s", getattr(user, 'phone_number', None))

    def send_event_reminder(self, users: List, event, send_sms: bool = True, send_email: bool = True):
        """
        Send event reminder to registered users

        Args:
            users: List of registered users
            event: Event object
            send_sms: Whether to send SMS reminders (default True)
        """
        time_diff = event.date - now()
        hours_until = int(time_diff.total_seconds() / 3600)

        for user in users:
            if send_email:
                try:
                    self.mail_service.send_event_reminder(user, event, self.site_url)
                except Exception:
                    logger.exception("Error sending reminder email to %s", getattr(user, 'email', None))
            if send_sms and hasattr(user, 'phone_number') and user.phone_number:
                try:
                    event_date = event.date.strftime("%b %d, %Y at %I:%M %p")
                    event_url = f"{self.site_url.rstrip('/')}/events/{event.slug}"
                    self.sms_service.send_event_reminder_sms(
                        user.phone_number,
                        event.title,
                        event_date,
                        hours_until,
                        event_url=event_url,
                    )
                except Exception as e:
                    logger.exception("Error sending reminder SMS to %s", getattr(user, 'phone_number', None))

    def send_upcoming_events_digest(self, users: List, events: List, send_sms: bool = False, send_email: bool = True):
        """
        Send digest of upcoming events

        Args:
            users: List of User objects
            events: List of Event objects
            send_sms: Whether to send SMS (default False for digests)
        """
        for user in users:
            if send_email:
                try:
                    self.mail_service.send_upcoming_events(user, events, self.site_url)
                except Exception:
                    logger.exception("Error sending events digest email to %s", getattr(user, 'email', None))

            if send_sms and hasattr(user, 'phone_number') and user.phone_number:
                try:
                    event_items = []
                    for ev in events[:3]:
                        when = getattr(ev, 'date', None)
                        when_text = when.strftime("%b %d") if when else "TBA"
                        title = getattr(ev, 'title', 'Event')
                        slug = getattr(ev, 'slug', None)
                        url = f"{self.site_url.rstrip('/')}/events/{slug}" if slug else f"{self.site_url.rstrip('/')}/events"
                        event_items.append({"title": title, "when": when_text, "url": url})

                    self.sms_service.send_upcoming_events_digest_sms(
                        user.phone_number,
                        event_items=event_items,
                        site_url=self.site_url,
                    )
                except Exception:
                    logger.exception("Error sending events digest SMS to %s", getattr(user, 'phone_number', None))

    def send_registration_confirmation(self, user, event, registration, send_sms: bool = True, send_email: bool = True):
        """
        Send registration confirmation

        Args:
            user: User object
            event: Event object
            registration: EventRegistration object
            send_sms: Whether to send SMS confirmation (default True)
        """
        if send_email:
            try:
                self.mail_service.send_registration_confirmation(user, event, registration, self.site_url)
            except Exception:
                logger.exception("Error sending registration confirmation email to %s", getattr(user, 'email', None))

        if send_sms and hasattr(user, 'phone_number') and user.phone_number:
            try:
                registration_code = getattr(registration, 'registration_code', None)
                event_url = f"{self.site_url.rstrip('/')}/events/{event.slug}"
                self.sms_service.send_registration_confirmation_sms(
                    user.phone_number,
                    event.title,
                    registration_code,
                    event_url=event_url,
                )
            except Exception as e:
                logger.exception("Error sending registration confirmation SMS to %s", getattr(user, 'phone_number', None))

    def send_new_location_login_alert(self, user, login_info: dict, send_sms: bool = True, send_email: bool = True):
        """
        Send security alert for new location login

        Args:
            user: User object
            login_info: Dictionary with login details (ip_address, location, device, browser, etc.)
            send_sms: Whether to send SMS alert (default True for security alerts)
        """
        if send_email:
            try:
                self.mail_service.send_new_location_login_alert(user, login_info, self.site_url)
            except Exception:
                logger.exception("Error sending login alert email to %s", getattr(user, 'email', None))

        if send_sms and hasattr(user, 'phone_number') and user.phone_number:
            try:
                location = login_info.get('location', 'Unknown location')
                time = login_info.get('login_time', now()).strftime("%b %d at %I:%M %p")
                self.sms_service.send_new_location_login_sms(
                    user.phone_number,
                    location,
                    time
                )
            except Exception as e:
                logger.exception("Error sending login alert SMS to %s", getattr(user, 'phone_number', None))
