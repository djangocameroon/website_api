from datetime import timedelta
from typing import List, Optional

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now

from utils import generate_otp


class MailService:
    def __init__(self, from_email=None):
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL

    def _new_mail(self):
        return EmailMessage(from_email=self.from_email)

    def send_mail(self, subject, message, to, attashment=None, context=None):
        mail = self._new_mail()
        mail.subject = subject
        if message.endswith('.html'):
            mail.body = render_to_string(message, context=context)
            mail.content_subtype = 'html'
        else:
            mail.body = message
        mail.to = to
        if attashment:
            mail.attach(attashment.name, attashment.read(), attashment.content_type)
        mail.send()

    def send_otp(self, reciever):
        mail = self._new_mail()
        mail.subject = "OTP Code"
        otp = generate_otp()
        reciever.otp_codes.create(otp_code=otp, expires_at=now() + timedelta(minutes=10))
        mail.body = render_to_string("mails/otp.html", context={"otp": otp})
        mail.content_subtype = 'html'
        mail.to = [reciever.email]
        mail.send()

    def verify_otp(self, reciever, otp_code):
        otp = reciever.otp_codes.filter(otp_code=otp_code).first()
        if not otp or otp.has_expired():
            return False
        otp.delete()
        return True

    def send_welcome_email(self, user, site_url: str = "https://djangocameroon.org"):
        """Send welcome email to new user"""
        mail = self._new_mail()
        mail.subject = "Welcome to Django Cameroon!"
        mail.body = render_to_string("mails/welcome.html", context={
            "user": user,
            "site_url": site_url
        })
        mail.content_subtype = 'html'
        mail.to = [user.email]
        mail.send()

    def send_signup_confirmation_email(self, user, site_url: str = "https://djangocameroon.org"):
        """Send signup/registration confirmation email to new user."""
        mail = self._new_mail()
        mail.subject = "Your Django Cameroon account is ready"
        mail.body = render_to_string("mails/signup_confirmation.html", context={
            "user": user,
            "site_url": site_url
        })
        mail.content_subtype = 'html'
        mail.to = [user.email]
        mail.send()

    def send_event_notification(self, user, event, site_url: str = "https://djangocameroon.org"):
        mail = self._new_mail()
        mail.subject = f"New Event: {event.title}"
        mail.body = render_to_string("mails/event_notification.html", context={
            "user": user,
            "event": event,
            "site_url": site_url
        })
        mail.content_subtype = 'html'
        mail.to = [user.email]

        filename, ics_content = event.get_calendar_ics()
        mail.attach(filename, ics_content, 'text/calendar')

        mail.send()

    def send_event_cancelled(self, user, event, cancellation_reason: Optional[str] = None,
                            reschedule_info: Optional[str] = None,
                            site_url: str = "https://djangocameroon.org"):
        """Send notification about event cancellation"""
        mail = self._new_mail()
        mail.subject = f"Event Cancelled: {event.title}"
        mail.body = render_to_string("mails/event_cancelled.html", context={
            "user": user,
            "event": event,
            "cancellation_reason": cancellation_reason,
            "reschedule_info": reschedule_info,
            "site_url": site_url
        })
        mail.content_subtype = 'html'
        mail.to = [user.email]
        mail.send()

    def send_event_reminder(self, user, event, site_url: str = "https://djangocameroon.org"):
        mail = self._new_mail()
        mail.subject = f"Reminder: {event.title}"
        mail.body = render_to_string("mails/event_reminder.html", context={
            "user": user,
            "event": event,
            "site_url": site_url
        })
        mail.content_subtype = 'html'
        mail.to = [user.email]

        filename, ics_content = event.get_calendar_ics()
        mail.attach(filename, ics_content, 'text/calendar')

        mail.send()

    def send_upcoming_events(self, user, events: List, site_url: str = "https://djangocameroon.org"):
        """Send digest of upcoming events"""
        mail = self._new_mail()
        mail.subject = "Upcoming Events This Month - Django Cameroon"
        mail.body = render_to_string("mails/upcoming_events.html", context={
            "user": user,
            "events": events,
            "site_url": site_url
        })
        mail.content_subtype = 'html'
        mail.to = [user.email]
        mail.send()

    def send_registration_confirmation(self, user, event, registration,
                                      site_url: str = "https://djangocameroon.org"):
        mail = self._new_mail()
        mail.subject = f"Registration Confirmed: {event.title}"
        mail.body = render_to_string("mails/registration_confirmation.html", context={
            "user": user,
            "event": event,
            "registration": registration,
            "site_url": site_url
        })
        mail.content_subtype = 'html'
        mail.to = [user.email]

        filename, ics_content = event.get_calendar_ics()
        mail.attach(filename, ics_content, 'text/calendar')

        mail.send()

    def send_new_location_login_alert(self, user, login_info: dict,
                                     site_url: str = "https://djangocameroon.org"):
        """Send security alert for new login"""
        mail = self._new_mail()
        mail.subject = "Security Alert: New Login Detected"
        mail.body = render_to_string("mails/new_location_login.html", context={
            "user": user,
            "login_time": login_info.get('login_time'),
            "ip_address": login_info.get('ip_address'),
            "location": login_info.get('location'),
            "device": login_info.get('device'),
            "browser": login_info.get('browser'),
            "site_url": site_url
        })
        mail.content_subtype = 'html'
        mail.to = [user.email]
        mail.send()
