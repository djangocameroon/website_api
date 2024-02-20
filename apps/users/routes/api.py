from django.urls import re_path
from apps.users.views.auth_view import UserRegistrationView, LoginView, PasswordResetRequestView, PasswordResetConfirmationView

urlpatterns = [
    re_path(r'^auth/register/$', UserRegistrationView.as_view(), name='register'),
    re_path(r'^auth/login/$', LoginView.as_view(), name='login'),
    re_path(r'^auth/password/reset/$', PasswordResetRequestView.as_view(), name='password-reset'),
    re_path(r'^auth/password/reset/confirm/$', PasswordResetConfirmationView.as_view(), name='password-reset-confirm'),
] 