from crequest.middleware import CrequestMiddleware
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.users.models import BaseModel


@receiver(pre_save, sender=BaseModel)
def update_user_id(sender, instance, **kwargs):
    """
    Signal to update the 'updated_by' and 'created_by' fields to the current user whenever a model instance is saved.
    """
    try:
        request = CrequestMiddleware.get_request()
        if request and request.user.is_authenticated:
            user = request.user
        else:
            user = None
    except Exception as e:
        user = None

    if not instance.created_by_id:
        instance.created_by = user

    instance.updated_by = user
