from django.contrib import admin

from apps.subs.models import Subscriber, SubscriptionVerificationToken

# Register your models here.
admin.site.register(Subscriber)
admin.site.register(SubscriptionVerificationToken)