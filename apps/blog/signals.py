from django.db.models.signals import pre_delete
from django.dispatch import receiver
from apps.blog.models.image import Image
import os

@receiver(pre_delete, sender=Image)
def delete_image_file(sender, instance, **kwargs):
    if instance.image_file:
        if os.path.isfile(instance.image_file.path):
            os.remove(instance.image_file.path)
