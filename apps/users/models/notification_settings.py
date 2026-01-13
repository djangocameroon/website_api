from django.db import models


class NotificationSettings(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True, default=1, editable=False)

    send_welcome_email = models.BooleanField(default=True)
    send_welcome_sms = models.BooleanField(default=False)

    send_signup_email = models.BooleanField(default=False)
    send_signup_sms = models.BooleanField(default=False)

    send_new_event_email = models.BooleanField(default=True)
    send_new_event_sms = models.BooleanField(default=False)

    send_event_cancelled_email = models.BooleanField(default=True)
    send_event_cancelled_sms = models.BooleanField(default=True)

    send_event_reminder_email = models.BooleanField(default=True)
    send_event_reminder_sms = models.BooleanField(default=True)

    send_upcoming_digest_email = models.BooleanField(default=True)
    send_upcoming_digest_sms = models.BooleanField(default=False)

    send_registration_confirmation_email = models.BooleanField(default=True)
    send_registration_confirmation_sms = models.BooleanField(default=True)

    send_new_location_login_email = models.BooleanField(default=True)
    send_new_location_login_sms = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.id = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        return cls.objects.first()

    def __str__(self):
        return "Notification Settings"

    class Meta:
        verbose_name = "Notification Settings"
        verbose_name_plural = "Notification Settings"