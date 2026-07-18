from rest_framework import serializers

from apps.events.models.speaker import Speaker, SpeakerSocialMedia

class SpeakerSocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeakerSocialMedia
        fields = ("id", "platform", "active", "profile_link")
        read_only_fields = ("id", "active", "platform")

class SpeakerSerializer(serializers.ModelSerializer):
    social_media = SpeakerSocialMediaSerializer(many=True, read_only=True)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["speciality"] = instance.speciality.name if instance.speciality else None
        rep['social_media'] = [social_media for social_media in rep['social_media'] if social_media['active']]
        return rep

    class Meta:
        model = Speaker
        exclude = ("active", "created_by", "updated_by")
        read_only_fields = ("id", "last_updated_by")
        


class SpeakerWithLastUpdatedBySerializer(serializers.ModelSerializer):
    social_media = SpeakerSocialMediaSerializer(many=True, read_only=True)

    class Meta:
        model = Speaker
        fields = "__all__"
        read_only_fields = ("id",)
