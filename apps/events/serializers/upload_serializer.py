from rest_framework import serializers


class UploadSerializer(serializers.Serializer):
    file = serializers.URLField()
