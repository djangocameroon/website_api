import secrets
from datetime import timedelta

from django.contrib.auth import authenticate
from django.utils.timezone import now
from oauth2_provider.models import AccessToken, RefreshToken, Application


def get_serializer(self, *args, **kwargs):
    return self.serializer_class(*args, **kwargs)


def authenticate_user(self, data):
    return authenticate(username=data['email_or_username'], password=data['password'])


def generate_tokens(self, user):
    application, _ = Application.objects.get_or_create(name="Default")
    expiration_time = now() + timedelta(days=1)

    access_token = AccessToken.objects.create(
        user=user,
        application=application,
        expires=expiration_time,
        token=secrets.token_hex(16),
    )
    refresh_token = RefreshToken.objects.create(
        user=user,
        application=application,
        token=secrets.token_hex(16),
        access_token=access_token,
    )
    return {'access_token': access_token, 'refresh_token': refresh_token}
