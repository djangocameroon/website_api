from django.urls import re_path

from apps.subs.views import (
    SendSubscriptionVerificationView,
    SubscriberCreateView,
    UnsubscribeView,
    VerifySubscriptionEmailView,
)

urlpatterns = [
    re_path(r'^subscribers/$', SubscriberCreateView.as_view(), name='subscriber-create'),
    re_path(r'^subscribers/verify/send/$', SendSubscriptionVerificationView.as_view(), name='subscriber-verify-send'),
    re_path(r'^subscribers/verify/$', VerifySubscriptionEmailView.as_view(), name='subscriber-verify'),
    re_path(r'^subscribers/unsubscribe/$', UnsubscribeView.as_view(), name='subscriber-unsubscribe'),
]
