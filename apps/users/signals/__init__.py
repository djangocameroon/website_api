from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from crequest.middleware import CrequestMiddleware

from apps.users.models import LoginHistory, BaseModel
from apps.users.tasks import send_new_location_login_alert_task, send_user_created_notifications_task

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Send welcome email to new users
    """
    if created:
        send_user_created_notifications_task.delay(instance.pk)


@receiver(user_logged_in)
def track_user_login(sender, request, user, **kwargs):
    """
    Track user login and detect new locations
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip_address = x_forwarded_for.split(',')[0]
    else:
        ip_address = request.META.get('REMOTE_ADDR')

    user_agent = request.META.get('HTTP_USER_AGENT', '')

    device_type = 'unknown'
    browser = 'Unknown'
    os = 'Unknown'

    if user_agent:
        user_agent_lower = user_agent.lower()
        if 'mobile' in user_agent_lower or 'android' in user_agent_lower or 'iphone' in user_agent_lower:
            device_type = 'mobile'
        elif 'tablet' in user_agent_lower or 'ipad' in user_agent_lower:
            device_type = 'tablet'
        else:
            device_type = 'desktop'

        if 'chrome' in user_agent_lower and 'edg' not in user_agent_lower:
            browser = 'Chrome'
        elif 'firefox' in user_agent_lower:
            browser = 'Firefox'
        elif 'safari' in user_agent_lower and 'chrome' not in user_agent_lower:
            browser = 'Safari'
        elif 'edg' in user_agent_lower:
            browser = 'Edge'

        if 'windows' in user_agent_lower:
            os = 'Windows'
        elif 'mac' in user_agent_lower:
            os = 'macOS'
        elif 'linux' in user_agent_lower:
            os = 'Linux'
        elif 'android' in user_agent_lower:
            os = 'Android'
        elif 'iphone' in user_agent_lower or 'ipad' in user_agent_lower:
            os = 'iOS'

    country = ''
    city = ''

    is_new_location = LoginHistory.is_new_login_location(user, ip_address, country, city)

    login_record = LoginHistory.objects.create(
        user=user,
        ip_address=ip_address,
        user_agent=user_agent,
        device_type=device_type,
        browser=browser,
        os=os,
        country=country,
        city=city,
        is_new_location=is_new_location,
        login_successful=True
    )

    if is_new_location:
        send_new_location_login_alert_task.delay(login_record.pk)


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
