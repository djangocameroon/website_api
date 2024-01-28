from rest_framework import serializers

from apps.events.models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "category",
            "for_community",
            "title",
            "description",
            "location",
            "hour",
            "date",
            "type",
            "speaker",
            "tags",
        )
