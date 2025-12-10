from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.timezone import now


class OtpCode(models.Model):
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=255)
    use_for = models.CharField(max_length=255, default="email")
    expires_at = models.DateTimeField()

    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        db_table = "otp_codes"
        verbose_name = "OTP Code"
        verbose_name_plural = "OTP Codes"

    def has_expired(self):
        return self.expires_at < now()
