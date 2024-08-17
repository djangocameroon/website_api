from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from rest_framework import serializers

from apps.events.models.event import Event
from apps.events.models.speaker import Speaker
from apps.events.serializers.speaker_serializer import SpeakerSerializer


class EventSerializer(serializers.ModelSerializer):
    speaker = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"

    @extend_schema_field(OpenApiTypes.STR)
    def get_speaker(self, event):
        speaker = Speaker.objects.get(id=event.speaker.id)
        return SpeakerSerializer(speaker).data


class CreateEventInputSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an event.
    This serializer is used to validate the input data.
    """

    class Meta:
        model = Event
        exclude = ("published", "created_by")


class CreateEventSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an event.
    This serializer is used to create the event.
    """

    class Meta:
        model = Event
        exclude = ("published",)
