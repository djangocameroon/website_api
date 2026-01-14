from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Q

User = get_user_model()


def authenticate_user(self, data):
    try:
        user = User.objects.get(Q(username=data['email_or_username']) | Q(email=data['email_or_username']))
        if user and user.check_password(data['password']):
            if not user.is_active:
                raise ValueError("Account is not active. Please verify your email to activate your account.")
            return user
        return None
    except User.DoesNotExist:
        raise ValueError("Authentication credentials invalid")


class EmailOrUsernameBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            return None

        if user.check_password(password) and user.is_active:
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
