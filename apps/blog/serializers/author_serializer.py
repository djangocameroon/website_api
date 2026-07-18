from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio')

    def __init__(self, *args, exclude_fields=None, only_fields=None, **kwargs):
        super().__init__(*args, **kwargs)
        if exclude_fields:
            for field in exclude_fields:
                self.fields.pop(field, None)

        if only_fields:
            allowed = set(only_fields)
            existing = set(self.fields.keys())
            for field in existing - allowed:
                self.fields.pop(field, None)
