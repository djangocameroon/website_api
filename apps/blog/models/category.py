from django.db import models
from apps.users.models.base_model import BaseModel

class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


