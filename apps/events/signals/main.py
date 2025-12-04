from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.events.models import Speaker, SpeakerSocialMedia

@receiver(post_save, sender=Speaker)
def update_speaker_social_media_active_status(sender, instance, **kwargs):
    social_media_accounts = SpeakerSocialMedia.objects.filter(speaker=instance)
    for account in social_media_accounts:
        account.active = instance.active
        account.save()