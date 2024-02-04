from django.db import models


class Speaker(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(null=True)     # Or we can use a URLField()
    # Social part
    twitter = models.CharField(max_length=50, null=True)
    linkedin = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)    # Maybe necessary for the Read More of the event

    def __str__(self):
        return self.full_name
