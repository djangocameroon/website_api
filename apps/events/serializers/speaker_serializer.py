from rest_framework import serializers

from apps.events.models.speaker import Speaker


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = "__all__"
        read_only_fields = ("id",)
