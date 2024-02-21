from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.fields import GenericRelation
from django.utils.translation import gettext_lazy as _
from apps.users.user_manager import UserManager
from services import MailService

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    profile_image = models.ImageField(upload_to="users", null=True, blank=True)
    otp_codes = GenericRelation('users.OtpCode')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def send_email_otp(self):
        mail_service = MailService()
        mail_service.send_otp(self)
