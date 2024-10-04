from django.db import models
from apps.users.models.base_model import BaseModel



class Author(BaseModel):
    name = models.CharField(max_length=100)
    bio = models.TextField()

    def __str__(self):
        return self.name


