from rest_framework import serializers
from apps.blog.models.tag import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
