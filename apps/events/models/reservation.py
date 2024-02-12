from django.db import models

from .event import Event


class Reservation(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name="reservations"
    )
    # Waiting for a User model
    # user = models.ForeignKey("User", on_delete=models.CASCADE)
    email = models.EmailField()
    full_name = models.CharField(max_length=100)
    sex = models.CharField(
        max_length=10,
        choices=(("Male", "Male"), ("Female", "Female")),
        default="Male",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    check_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} -> {self.event.title}"
