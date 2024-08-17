from crequest.middleware import CrequestMiddleware
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.users.models import BaseModel


@receiver(pre_save, sender=BaseModel)
def update_user_id(sender, instance, **kwargs):
    """
    Signal to update the 'updated_by' field to the current user whenever a model instance is saved.
    This assumes that you have access to the request object to determine the current user.
    """
    try:
        request = CrequestMiddleware.get_request()
        user = request.user if request else None
    except:
        user = None

    if not instance.created_by_id:
        instance.created_by = user
    instance.updated_by = user
