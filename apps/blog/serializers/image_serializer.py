from rest_framework import serializers
from apps.blog.models.image import Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
