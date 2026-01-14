from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models.base_model import BaseModel


class LoginHistory(BaseModel):
    """Track user login history for security monitoring"""

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='login_history',
        verbose_name=_("User"),
        help_text=_("The user who logged in")
    )
    ip_address = models.GenericIPAddressField(
        verbose_name=_("IP Address"),
        help_text=_("IP address of the login")
    )
    user_agent = models.TextField(
        blank=True,
        verbose_name=_("User Agent"),
        help_text=_("Browser user agent string")
    )
    device_type = models.CharField(
        max_length=50,
        blank=True,
        choices=(
            ('desktop', 'Desktop'),
            ('mobile', 'Mobile'),
            ('tablet', 'Tablet'),
            ('unknown', 'Unknown'),
        ),
        default='unknown',
        verbose_name=_("Device Type")
    )
    browser = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Browser"),
        help_text=_("Browser name and version")
    )
    os = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Operating System"),
        help_text=_("Operating system name and version")
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Country"),
        help_text=_("Country from IP geolocation")
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("City"),
        help_text=_("City from IP geolocation")
    )
    is_new_location = models.BooleanField(
        default=False,
        verbose_name=_("New Location"),
        help_text=_("Whether this is a login from a new location")
    )
    login_successful = models.BooleanField(
        default=True,
        verbose_name=_("Login Successful"),
        help_text=_("Whether the login was successful")
    )
    notification_sent = models.BooleanField(
        default=False,
        verbose_name=_("Notification Sent"),
        help_text=_("Whether a notification was sent for this login")
    )

    class Meta:
        db_table = 'login_history'
        verbose_name = _("Login History")
        verbose_name_plural = _("Login Histories")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['ip_address']),
            models.Index(fields=['is_new_location']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.ip_address} at {self.created_at}"

    @classmethod
    def is_new_login_location(cls, user, ip_address, country=None, city=None):
        """
        Check if this is a new login location for the user

        Args:
            user: User object
            ip_address: IP address of current login
            country: Country from geolocation (optional)
            city: City from geolocation (optional)

        Returns:
            bool: True if this is a new location
        """
        # Check if user has logged in from this IP before
        if cls.objects.filter(user=user, ip_address=ip_address, login_successful=True).exists():
            return False

        # If we have location data, check if user has logged in from this location
        if country:
            if cls.objects.filter(
                user=user,
                country=country,
                city=city if city else '',
                login_successful=True
            ).exists():
                return False

        return True

    @classmethod
    def get_location_string(cls, country, city):
        """Format location string for notifications"""
        if city and country:
            return f"{city}, {country}"
        elif country:
            return country
        return "Unknown location"
