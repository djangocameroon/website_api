import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.users.models.base_model import BaseModel


class EventRegistration(BaseModel):
    """Track user registrations for events"""

    event = models.ForeignKey(
        'Event',
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name=_("Event"),
        help_text=_("The event being registered for")
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='event_registrations',
        verbose_name=_("User"),
        help_text=_("The user registering for the event")
    )
    registration_code = models.CharField(
        max_length=20,
        unique=True,
        verbose_name=_("Registration Code"),
        help_text=_("Unique registration code for check-in")
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('registered', 'Registered'),
            ('attended', 'Attended'),
            ('cancelled', 'Cancelled'),
            ('no_show', 'No Show'),
        ),
        default='registered',
        verbose_name=_("Status"),
        help_text=_("Registration status")
    )
    checked_in = models.BooleanField(
        default=False,
        verbose_name=_("Checked In"),
        help_text=_("Whether the user has checked in")
    )
    check_in_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Check-in Time"),
        help_text=_("Time when user checked in")
    )
    reminder_sent = models.BooleanField(
        default=False,
        verbose_name=_("Reminder Sent"),
        help_text=_("Whether a reminder has been sent")
    )
    confirmation_sent = models.BooleanField(
        default=False,
        verbose_name=_("Confirmation Sent"),
        help_text=_("Whether a confirmation email has been sent")
    )
    notes = models.TextField(
        blank=True,
        verbose_name=_("Notes"),
        help_text=_("Additional notes or special requirements")
    )

    class Meta:
        db_table = 'event_registrations'
        verbose_name = _("Event Registration")
        verbose_name_plural = _("Event Registrations")
        unique_together = ('event', 'user')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['event', 'status']),
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['registration_code']),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.event.title}"

    def save(self, *args, **kwargs):
        if not self.registration_code:
            self.registration_code = self.generate_registration_code()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_registration_code():
        """Generate a unique registration code"""
        return f"REG-{uuid.uuid4().hex[:8].upper()}"

    def mark_as_attended(self):
        """Mark this registration as attended"""
        from django.utils.timezone import now
        self.status = 'attended'
        self.checked_in = True
        self.check_in_time = now()
        self.save()

    def cancel_registration(self):
        """Cancel this registration"""
        self.status = 'cancelled'
        self.save()


class EventAttendanceStats(BaseModel):
    """Store attendance statistics for events"""

    event = models.OneToOneField(
        'Event',
        on_delete=models.CASCADE,
        related_name='attendance_stats',
        verbose_name=_("Event")
    )
    total_registered = models.IntegerField(
        default=0,
        verbose_name=_("Total Registered"),
        help_text=_("Total number of registrations")
    )
    total_attended = models.IntegerField(
        default=0,
        verbose_name=_("Total Attended"),
        help_text=_("Total number of attendees who showed up")
    )
    total_cancelled = models.IntegerField(
        default=0,
        verbose_name=_("Total Cancelled"),
        help_text=_("Total number of cancelled registrations")
    )
    total_no_show = models.IntegerField(
        default=0,
        verbose_name=_("Total No Show"),
        help_text=_("Total number of no-shows")
    )

    class Meta:
        db_table = 'event_attendance_stats'
        verbose_name = _("Event Attendance Stats")
        verbose_name_plural = _("Event Attendance Stats")

    def __str__(self):
        return f"Stats for {self.event.title}"

    def update_stats(self):
        """Update attendance statistics"""
        registrations = self.event.registrations.all()
        self.total_registered = registrations.filter(status='registered').count()
        self.total_attended = registrations.filter(status='attended').count()
        self.total_cancelled = registrations.filter(status='cancelled').count()
        self.total_no_show = registrations.filter(status='no_show').count()
        self.save()

    @property
    def attendance_rate(self):
        """Calculate attendance rate"""
        total = self.total_registered + self.total_attended + self.total_no_show
        if total == 0:
            return 0
        return (self.total_attended / total) * 100
