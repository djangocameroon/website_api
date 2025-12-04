from datetime import timedelta

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now

from utils import generate_otp


class MailService:
    def __init__(self, from_email=None):
        self.mail = EmailMessage()
        if from_email:
            self.mail.from_email = from_email
        else:
            self.mail.from_email = settings.DEFAULT_FROM_EMAIL

    def send_mail(self, subject, message, to, attashment=None, context=None):
        self.mail.subject = subject
        if message.endswith('.html'):
            self.mail.body = render_to_string(message, context=context)
            self.mail.content_subtype = 'html'
        else:
            self.mail.body = message
        self.mail.to = to
        if attashment:
            self.mail.attach(attashment.name, attashment.read(), attashment.content_type)
        self.mail.send()

    def send_otp(self, reciever):
        self.mail.subject = "OTP Code"
        otp = generate_otp()
        reciever.otp_codes.create(otp_code=otp, expires_at=now() + timedelta(minutes=10))
        self.mail.body = render_to_string("mails/otp.html", context={"otp": otp})
        self.mail.content_subtype = 'html'
        self.mail.to = [reciever.email]
        self.mail.send()

    def verify_otp(self, reciever, otp_code):
        otp = reciever.otp_codes.filter(otp_code=otp_code).first()
        if not otp or otp.has_expired():
            return False
        otp.delete()
        return True
