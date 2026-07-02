from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from rest_framework import serializers

from apps.events.models import Event, EventCity, EventRegion, Speaker, EventTag, EventVenue
from apps.events.models.constants import EventType
from apps.events.serializers.speaker_serializer import SpeakerSerializer


class EventRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegion
        fields = ("id", "name")


class EventCitySerializer(serializers.ModelSerializer):
    region = EventRegionSerializer()

    class Meta:
        model = EventCity
        fields = ("id", "name", "region")


class EventVenueSerializer(serializers.ModelSerializer):
    city = EventCitySerializer()

    class Meta:
        model = EventVenue
        fields = ("id", "name", "city")


class EventSerializer(serializers.ModelSerializer):
    speakers_data = serializers.SerializerMethodField()
    tags_list = serializers.SerializerMethodField()
    location_data = serializers.SerializerMethodField()

    class Meta:
        model = Event
        exclude = ("active", "level", "speakers", "tags", "location", "created_by", "updated_by")

    @extend_schema_field(OpenApiTypes.STR)
    def get_speakers_data(self, event):
        try:
            return [SpeakerSerializer(speaker).data for speaker in event.speakers.all()]
        except:
            return []

    @extend_schema_field(OpenApiTypes.STR)
    def get_tags_list(self, event):
        try:
            return [tag.name for tag in event.tags.all()]
        except:
            return []

    @extend_schema_field(OpenApiTypes.STR)
    def get_location_data(self, event):
        try:
            return EventVenueSerializer(event.location).data
        except:
            return None


class CreateEventInputSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an event.
    This serializer is used to validate the input data.
    """
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    speakers = serializers.ListField(child=serializers.CharField(), required=False)
    thumbnail = serializers.ImageField(required=False)
    location = serializers.PrimaryKeyRelatedField(
        queryset=EventVenue.objects.all(), required=False, allow_null=True, default=None,
    )

    class Meta:
        model = Event
        exclude = ("created_by", "id", "active", "slug", "level",)

    def validate(self, data):
        event_type = data.get("type", getattr(self.instance, "type", None))
        location = data.get("location", getattr(self.instance, "location", None))
        if event_type != EventType.ONLINE and location is None:
            raise serializers.ValidationError(
                {"location": _("Event location is required unless the event type is Online.")}
            )
        return data

    def validate_tags(self, tags):
        validated_tags = []
        for tag in tags:
            tag_obj, created = EventTag.objects.get_or_create(name=tag)
            validated_tags.append(tag_obj)
        return validated_tags

    def validate_speakers(self, speaker_ids):
        speakers = Speaker.objects.filter(id__in=speaker_ids)
        if len(speakers) != len(speaker_ids):
            raise serializers.ValidationError(
                _("One or more speaker IDs are invalid.")
            )
        return list(speakers)

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        speakers = validated_data.pop('speakers', [])
        event = super().create(validated_data)
        event.tags.set(tags)
        event.speakers.set(speakers)
        return event

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = [tag.name for tag in instance.tags.all()]
        data['speakers'] = [speaker.name for speaker in instance.speakers.all()]
        return data


class CreateEventSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an event.
    This serializer is used to create the event.
    """

    class Meta:
        model = Event
        exclude = ("id",)
