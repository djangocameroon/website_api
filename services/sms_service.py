import os
from typing import Optional
from django.template.loader import render_to_string
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


class SMSTemplates:
    """SMS message templates for various notifications"""

    @staticmethod
    def welcome(user_name: str) -> str:
        return f"Welcome to Django Cameroon, {user_name}! We're excited to have you in our community. Visit djangocameroon.site to explore events."

    @staticmethod
    def signup_confirmation(user_name: str) -> str:
        return f"Hi {user_name}, your Django Cameroon account is ready. Log in at djangocameroon.site to complete your profile and join upcoming events."

    @staticmethod
    def event_notification(event_title: str, event_date: str, event_location: str, event_url: Optional[str] = None) -> str:
        base = f"New Event: {event_title} on {event_date} at {event_location}."
        if event_url:
            return f"{base} {event_url}"
        return f"{base} Register now at djangocameroon.site"

    @staticmethod
    def event_cancelled(event_title: str, event_date: str, event_url: Optional[str] = None) -> str:
        base = f"CANCELLED: {event_title} scheduled for {event_date} has been cancelled."
        if event_url:
            return f"{base} {event_url}"
        return f"{base} Check your email for details."

    @staticmethod
    def event_reminder(event_title: str, event_date: str, hours_until: int, event_url: Optional[str] = None) -> str:
        if hours_until <= 1:
            time_text = "in less than 1 hour"
        elif hours_until < 24:
            time_text = f"in {hours_until} hours"
        else:
            days = hours_until // 24
            time_text = f"in {days} day{'s' if days > 1 else ''}"
        base = f"Reminder: {event_title} starts {time_text}!"
        if event_url:
            return f"{base} {event_url}"
        return f"{base} See you there!"

    @staticmethod
    def registration_confirmation(
        event_title: str,
        registration_code: Optional[str] = None,
        event_url: Optional[str] = None,
    ) -> str:
        base_msg = f"Registration confirmed for {event_title}!"
        if registration_code:
            base_msg += f" Your code: {registration_code}"
        if event_url:
            base_msg += f" {event_url}"
        else:
            base_msg += " Check your email for details."
        return base_msg

    @staticmethod
    def new_location_login(location: str, time: str) -> str:
        return f"Security Alert: New login detected from {location} at {time}. If this wasn't you, secure your account immediately."

    @staticmethod
    def otp(otp_code: str) -> str:
        return f"Your Django Cameroon verification code is: {otp_code}. This code expires in 10 minutes."

    @staticmethod
    def upcoming_events_digest(event_items: list[dict], site_url: str = "djangocameroon.site") -> str:
        if not event_items:
            return f"Upcoming events: {site_url}/events"

        parts: list[str] = []
        for item in event_items[:3]:
            title = item.get('title') or 'Event'
            when = item.get('when') or 'TBA'
            url = item.get('url')
            if url:
                parts.append(f"{title} ({when}): {url}")
            else:
                parts.append(f"{title} ({when})")

        return f"Upcoming events: {'; '.join(parts)} More: {site_url}/events"


class SMSService:
    """Service for sending SMS notifications via Twilio"""

    def __init__(self):
        self.account_sid = os.getenv('TWILIO_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.verify_service_sid = os.getenv('TWILIO_VERIFY_SERVICE_SID')
        self.from_number = os.getenv('TWILIO_PHONE_NUMBER')

        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
        else:
            self.client = None

    def is_configured(self) -> bool:
        """Check if Twilio is properly configured"""
        return self.client is not None and self.from_number is not None

    def render_sms_template(self, template_name: str, context: dict, fallback_message: str) -> str:
        try:
            message = render_to_string(template_name, context=context)
            message = message.strip("\n")
            lines = [ln.rstrip() for ln in message.splitlines()]
            return "\n".join(lines).strip()
        except Exception:
            return fallback_message

    def send_sms(self, to_number: str, message: str) -> dict:
        """
        Send an SMS message

        Args:
            to_number: Phone number in E.164 format (e.g., +237XXXXXXXXX)
            message: Message content (max 160 chars for single SMS)

        Returns:
            dict with status and message_sid or error
        """
        if not self.is_configured():
            return {
                'success': False,
                'error': 'SMS service not configured. Please set TWILIO credentials in .env'
            }

        try:
            # Ensure phone number is in E.164 format
            if not to_number.startswith('+'):
                to_number = f'+{to_number}'

            message = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )

            return {
                'success': True,
                'message_sid': message.sid,
                'status': message.status
            }
        except TwilioRestException as e:
            return {
                'success': False,
                'error': str(e),
                'error_code': e.code
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }

    def send_welcome_sms(self, to_number: str, user_name: str) -> dict:
        """Send welcome SMS to new user"""
        fallback = SMSTemplates.welcome(user_name)
        message = self.render_sms_template(
            "sms/welcome.txt",
            context={"user_name": user_name},
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def send_signup_confirmation_sms(self, to_number: str, user_name: str) -> dict:
        """Send signup/registration confirmation SMS"""
        fallback = SMSTemplates.signup_confirmation(user_name)
        message = self.render_sms_template(
            "sms/signup_confirmation.txt",
            context={"user_name": user_name},
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def send_event_notification_sms(
        self,
        to_number: str,
        event_title: str,
        event_date: str,
        event_location: str,
        event_url: Optional[str] = None,
    ) -> dict:
        """Send event notification SMS"""
        fallback = SMSTemplates.event_notification(event_title, event_date, event_location, event_url=event_url)
        message = self.render_sms_template(
            "sms/event_notification.txt",
            context={
                "event_title": event_title,
                "event_date": event_date,
                "event_location": event_location,
                "event_url": event_url,
            },
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def send_event_cancelled_sms(
        self,
        to_number: str,
        event_title: str,
        event_date: str,
        event_url: Optional[str] = None,
    ) -> dict:
        """Send event cancellation SMS"""
        fallback = SMSTemplates.event_cancelled(event_title, event_date, event_url=event_url)
        message = self.render_sms_template(
            "sms/event_cancelled.txt",
            context={"event_title": event_title, "event_date": event_date, "event_url": event_url},
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def send_event_reminder_sms(
        self,
        to_number: str,
        event_title: str,
        event_date: str,
        hours_until: int,
        event_url: Optional[str] = None,
    ) -> dict:
        """Send event reminder SMS"""
        if hours_until <= 1:
            time_text = "in less than 1 hour"
        elif hours_until < 24:
            time_text = f"in {hours_until} hours"
        else:
            days = hours_until // 24
            time_text = f"in {days} day{'s' if days > 1 else ''}"

        fallback = SMSTemplates.event_reminder(event_title, event_date, hours_until, event_url=event_url)
        message = self.render_sms_template(
            "sms/event_reminder.txt",
            context={
                "event_title": event_title,
                "event_date": event_date,
                "time_text": time_text,
                "event_url": event_url,
            },
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def send_registration_confirmation_sms(self, to_number: str, event_title: str,
                                          registration_code: Optional[str] = None,
                                          event_url: Optional[str] = None) -> dict:
        """Send registration confirmation SMS"""
        fallback = SMSTemplates.registration_confirmation(event_title, registration_code, event_url=event_url)
        message = self.render_sms_template(
            "sms/registration_confirmation.txt",
            context={
                "event_title": event_title,
                "registration_code": registration_code,
                "event_url": event_url,
            },
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def send_new_location_login_sms(self, to_number: str, location: str, time: str) -> dict:
        """Send new location login alert SMS"""
        fallback = SMSTemplates.new_location_login(location, time)
        message = self.render_sms_template(
            "sms/new_location_login.txt",
            context={"location": location, "time": time},
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def send_otp_sms(self, to_number: str, otp_code: str) -> dict:
        """Send OTP code via SMS"""
        fallback = SMSTemplates.otp(otp_code)
        message = self.render_sms_template(
            "sms/otp.txt",
            context={"otp_code": otp_code},
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def send_upcoming_events_digest_sms(self, to_number: str, event_items: list[dict], site_url: str) -> dict:
        """Send a short upcoming-events digest via SMS (keeps content compact)."""
        cleaned_site = site_url.replace("https://", "").replace("http://", "").rstrip("/")
        fallback = SMSTemplates.upcoming_events_digest(event_items, site_url=cleaned_site)
        message = self.render_sms_template(
            "sms/upcoming_events_digest.txt",
            context={"event_items": event_items[:3], "site_url": cleaned_site},
            fallback_message=fallback,
        )
        return self.send_sms(to_number, message)

    def verify_phone_number(self, phone_number: str) -> dict:
        """
        Start phone number verification process using Twilio Verify

        Args:
            phone_number: Phone number to verify

        Returns:
            dict with status
        """
        if not self.verify_service_sid:
            return {
                'success': False,
                'error': 'Twilio Verify service not configured'
            }

        try:
            verification = self.client.verify \
                .v2 \
                .services(self.verify_service_sid) \
                .verifications \
                .create(to=phone_number, channel='sms')

            return {
                'success': True,
                'status': verification.status
            }
        except TwilioRestException as e:
            return {
                'success': False,
                'error': str(e)
            }

    def check_verification_code(self, phone_number: str, code: str) -> dict:
        """
        Check verification code for phone number

        Args:
            phone_number: Phone number being verified
            code: Verification code entered by user

        Returns:
            dict with verification status
        """
        if not self.verify_service_sid:
            return {
                'success': False,
                'error': 'Twilio Verify service not configured'
            }

        try:
            verification_check = self.client.verify \
                .v2 \
                .services(self.verify_service_sid) \
                .verification_checks \
                .create(to=phone_number, code=code)

            return {
                'success': verification_check.status == 'approved',
                'status': verification_check.status
            }
        except TwilioRestException as e:
            return {
                'success': False,
                'error': str(e)
            }
