from django.contrib import admin

from apps.users.models import NotificationSettings, OtpCode, User

admin.site.register(User)
admin.site.register(OtpCode)


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
	list_display = (
		'id',
		'send_welcome_email',
		'send_welcome_sms',
		'send_signup_email',
		'send_signup_sms',
		'send_new_event_sms',
		'send_event_cancelled_sms',
		'send_event_reminder_sms',
		'send_upcoming_digest_sms',
		'send_registration_confirmation_sms',
		'send_new_location_login_sms',
		'updated_at',
	)

	def has_add_permission(self, request):
		if NotificationSettings.objects.exists():
			return False
		return super().has_add_permission(request)

	def has_delete_permission(self, request, obj=None):
		return False
