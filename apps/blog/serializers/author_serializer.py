from rest_framework import serializers
from apps.blog.models.author import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'bio')
