from rest_framework import serializers

from apps.subs.models import Subscriber


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['email', 'is_verified', 'created_at']
        read_only_fields = ['is_verified']


class SendVerificationEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.strip().lower()


class VerifySubscriptionTokenSerializer(serializers.Serializer):
    token = serializers.CharField()


class UnsubscribeSerializer(serializers.Serializer):
    token = serializers.CharField()