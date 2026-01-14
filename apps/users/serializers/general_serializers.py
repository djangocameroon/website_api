from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class PaginationSerializer(serializers.Serializer):
    next = serializers.CharField()
    previous = serializers.CharField()
    count = serializers.IntegerField()
    current_page = serializers.IntegerField()
    total_pages = serializers.IntegerField()


class SuccessResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=True)
    message = serializers.CharField(max_length=200)
    status_code = serializers.IntegerField(default=200)

    def __init__(self, *args, **kwargs):
        data_serializer_class = kwargs.pop('data_serializer_class', None)
        many = kwargs.pop('many', False)
        super().__init__(*args, **kwargs)
        if data_serializer_class:
            self.fields['data'] = data_serializer_class(many=many)


class PaginatedResponseSerializer(SuccessResponseSerializer):
    next = serializers.CharField(required=False, allow_null=True)
    previous = serializers.CharField(required=False, allow_null=True)
    count = serializers.IntegerField()
    page = serializers.IntegerField()
    page_size = serializers.IntegerField()
    total_pages = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ErrorResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(default=False)
    message = serializers.CharField(default="An error occurred")
    status_code = serializers.IntegerField(default=400)

    def __init__(self, *args, **kwargs):
        default_message = kwargs.pop('default_message', None)
        super().__init__(*args, **kwargs)
        if default_message:
            self.fields['message'].default = default_message


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "profile_image",
            "first_name",
            "last_name",
            "last_login",
        ]


class UserMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "profile_image", "gender")


class SocialAccountSerializer(serializers.Serializer):
    platform = serializers.CharField(source='platform.name')
    link = serializers.URLField()


class OrganizerSerializer(serializers.ModelSerializer):
    social_accounts = SocialAccountSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "profile_image",
            "bio",
            "social_accounts"
        ]
