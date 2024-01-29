from django.urls import re_path
from apps.users.views.auth_view import UserRegistrationView

urlpatterns = [
    re_path(r'^auth/register/$', UserRegistrationView.as_view(), name='register')
] 