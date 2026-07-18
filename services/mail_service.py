from datetime import timedelta
from typing import List, Optional

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now
from email.utils import formataddr

from utils import generate_otp


class MailService:
    def __init__(self, from_email=None, display_name=None):
        self.from_email = from_email or settings.DEFAULT_FROM_EMAIL
        self.display_name = display_name or str(settings.EMAIL_DISPLAY_NAME) or None

    def _new_mail(self):
        from_email = self.from_email
        if self.display_name:
            from_email = formataddr((self.display_name, self.from_email))
        return EmailMessage(from_email=from_email)

    def send_mail(self, subject, message, to, attashment=None, context=None):
        mail = self._new_mail()
        mail.subject = subject
        if message.endswith('.html'):
            mail.body = render_to_string(message, context=context)
            mail.content_subtype = 'html'
        else:
            mail.body = message
        mail.to = to
        
        for attachment in (attashment if isinstance(attashment, list) else [attashment]):
            if attachment is None:
                continue
            if isinstance(attachment, tuple):
                filename, content, mimetype = attachment
                mail.attach(filename, content, mimetype)
            else:
                mail.attach(attachment.name, attachment.read(), attachment.content_type)
        mail.send()

    def send_otp(self, reciever):
        otp = generate_otp()
        reciever.otp_codes.create(otp_code=otp, expires_at=now() + timedelta(minutes=10))
        self.send_mail("OTP Code", "mails/otp.html", [reciever.email], context={"otp": otp})

    def verify_otp(self, reciever, otp_code):
        otp = reciever.otp_codes.filter(otp_code=otp_code).first()
        if not otp or otp.has_expired():
            return False
        otp.delete()
        return True

    def send_welcome_email(self, user, site_url: str = "https://djangocameroon.org"):
        """Send welcome email to new user"""
        self.send_mail("Welcome to Django Cameroon!", "mails/welcome.html", [user.email], context={
            "user": user,
            "site_url": site_url
        })

    def send_signup_confirmation_email(self, user, site_url: str = "https://djangocameroon.org"):
        """Send signup/registration confirmation email to new user."""
        self.send_mail("Your Django Cameroon account is ready", "mails/signup_confirmation.html", [user.email], context={
            "user": user,
            "site_url": site_url
        })

    def send_event_notification(self, user, event, site_url: str = "https://djangocameroon.org"):
        filename, ics_content = event.get_calendar_ics()
        self.send_mail(f"New Event: {event.title}", "mails/event_notification.html", [user.email],
                       attashment=(filename, ics_content, 'text/calendar'), context={
            "user": user,
            "event": event,
            "site_url": site_url
        })

    def send_event_cancelled(self, user, event, cancellation_reason: Optional[str] = None,
                            reschedule_info: Optional[str] = None,
                            site_url: str = "https://djangocameroon.org"):
        """Send notification about event cancellation"""
        self.send_mail(f"Event Cancelled: {event.title}", "mails/event_cancelled.html", [user.email], context={
            "user": user,
            "event": event,
            "cancellation_reason": cancellation_reason,
            "reschedule_info": reschedule_info,
            "site_url": site_url
        })

    def send_event_reminder(self, user, event, site_url: str = "https://djangocameroon.org"):
        filename, ics_content = event.get_calendar_ics()
        self.send_mail(f"Reminder: {event.title}", "mails/event_reminder.html", [user.email],
                       attashment=(filename, ics_content, 'text/calendar'), context={
            "user": user,
            "event": event,
            "site_url": site_url
        })

    def send_upcoming_events(self, user, events: List, site_url: str = "https://djangocameroon.org"):
        """Send digest of upcoming events"""
        self.send_mail("Upcoming Events This Month - Django Cameroon", "mails/upcoming_events.html", [user.email], context={
            "user": user,
            "events": events,
            "site_url": site_url
        })

    def send_registration_confirmation(self, user, event, registration,
                                      site_url: str = "https://djangocameroon.org"):
        filename, ics_content = event.get_calendar_ics()
        self.send_mail(f"Registration Confirmed: {event.title}", "mails/registration_confirmation.html", [user.email],
                       attashment=(filename, ics_content, 'text/calendar'), context={
            "user": user,
            "event": event,
            "registration": registration,
            "site_url": site_url
        })

    def send_subscription_verification_email(self, email: str, verification_url: str):
        """Send email verification link to a newsletter subscriber."""
        self.send_mail(
            "Confirm your subscription - Django Cameroon",
            "mails/subscription_verification.html",
            [email],
            context={"verification_url": verification_url}
        )

    def send_new_location_login_alert(self, user, login_info: dict,
                                     site_url: str = "https://djangocameroon.org"):
        """Send security alert for new login"""
        self.send_mail("Security Alert: New Login Detected", "mails/new_location_login.html", [user.email], context={
            "user": user,
            "login_time": login_info.get('login_time'),
            "ip_address": login_info.get('ip_address'),
            "location": login_info.get('location'),
            "device": login_info.get('device'),
            "browser": login_info.get('browser'),
            "site_url": site_url
        })
