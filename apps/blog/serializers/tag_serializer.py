from rest_framework import serializers
from apps.blog.models.tag import BlogTag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogTag
        fields = '__all__'
