from rest_framework import serializers

from apps.events.models.event import Event
from apps.events.models.speaker import Speaker
from apps.events.serializers.speaker_serializer import SpeakerSerializer


class EventSerializer(serializers.ModelSerializer):
    speaker = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"

    def get_speaker(self, event):
        speaker = Speaker.objects.get(id=event.speaker.id)
        return SpeakerSerializer(speaker).data


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ("published",)
