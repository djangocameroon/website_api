from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from rest_framework import serializers

from apps.events.models import Event, Speaker, EventTag, EventVenue
from apps.events.serializers.speaker_serializer import SpeakerSerializer


class EventSerializer(serializers.ModelSerializer):
    speakers = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Event
        exclude = ("active", "level",)

    @extend_schema_field(OpenApiTypes.STR)
    def get_speakers(self, event):
        speakers = Speaker.objects.filter(id__in=event.speakers.values_list('id', flat=True))
        return SpeakerSerializer(speakers, many=True).data

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tags'] = [tag.name for tag in instance.tags.all()]
        data['speakers'] = [SpeakerSerializer(speaker).data for speaker in instance.speakers.all()]
        return data


class CreateEventInputSerializer(serializers.ModelSerializer):
    """
    Serializer for creating an event.
    This serializer is used to validate the input data.
    """
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    speakers = serializers.ListField(child=serializers.CharField(), required=False)
    thumbnail = serializers.ImageField(required=False)

    class Meta:
        model = Event
        exclude = ("created_by", "id", "active", "slug", "level",)

    def validate(self, data):
        if not EventVenue.objects.filter(id=data["location"].id).exists():
            raise serializers.ValidationError(_("Invalid location ID."))
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
