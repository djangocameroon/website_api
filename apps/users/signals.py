from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from apps.users.models import LoginHistory
from services import NotificationService
from services.notification_preferences import get_notification_preferences

User = get_user_model()


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """
    Send welcome email to new users
    """
    if created:
        prefs = get_notification_preferences()
        notification_service = NotificationService()
        notification_service.send_welcome_notification(
            instance,
            send_sms=prefs.send_welcome_sms,
            send_email=prefs.send_welcome_email,
        )

        if prefs.send_signup_email or prefs.send_signup_sms:
            notification_service.send_signup_registration_notification(
                instance,
                send_sms=prefs.send_signup_sms,
                send_email=prefs.send_signup_email,
            )


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
        prefs = get_notification_preferences()
        notification_service = NotificationService()
        location_string = LoginHistory.get_location_string(country, city)
        if not location_string or location_string == "Unknown location":
            location_string = ip_address

        login_info = {
            'login_time': login_record.created_at,
            'ip_address': ip_address,
            'location': location_string,
            'device': f"{device_type.capitalize()}" if device_type != 'unknown' else None,
            'browser': browser if browser != 'Unknown' else None,
        }

        notification_service.send_new_location_login_alert(
            user,
            login_info,
            send_sms=prefs.send_new_location_login_sms,
            send_email=prefs.send_new_location_login_email,
        )
        login_record.notification_sent = True
        login_record.save(update_fields=['notification_sent'])
