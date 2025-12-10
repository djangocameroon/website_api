from django.contrib import admin

from apps.users.models import OtpCode, User

admin.site.register(User)
admin.site.register(OtpCode)
