from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from rest_framework import serializers

from apps.blog.models import Post, Tag, Category


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ("status", "post_id")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "name"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "name"