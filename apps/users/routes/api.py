from django.urls import re_path
from apps.users.views.auth_view import UserRegistrationView, LoginView, PasswordResetRequestView, PasswordResetConfirmationView, LogoutView, EmailVerificationView
from apps.users.views.user_views import UserDetails, UpdateUserProfile, OrganizersListView

urlpatterns = [
    re_path(r'^auth/register/$', UserRegistrationView.as_view(), name='register'),
    re_path(r'^auth/verify-email/$', EmailVerificationView.as_view(), name='verify-email'),
    re_path(r'^auth/login/$', LoginView.as_view(), name='login'),
    re_path(r'^auth/logout/$', LogoutView.as_view(), name='logout'),
    re_path(r'^auth/password/reset/$', PasswordResetRequestView.as_view(), name='password-reset'),
    re_path(r'^auth/password/reset/confirm/$', PasswordResetConfirmationView.as_view(), name='password-reset-confirm'),

    re_path(r'^user/$', UserDetails.as_view(), name='user-details'),
    re_path(r'^user/profile/$', UpdateUserProfile.as_view(), name='update-user-profile'),
    re_path(r'^organizers/$', OrganizersListView.as_view(), name='organizers-list'),
] 