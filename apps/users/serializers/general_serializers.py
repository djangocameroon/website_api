from rest_framework import serializers

class SuccessResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=True)
    message = serializers.CharField(max_length=255)
    data = serializers.JSONField(required=False)

class ErrorResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=True)
    message = serializers.CharField(max_length=255)
    errors = serializers.JSONField(required=False)
