from rest_framework import serializers
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError

from apps.blog.models.blog import Blog
from apps.blog.models.tag import BlogTag
from apps.blog.serializers.author_serializer import AuthorSerializer
from apps.blog.serializers.tag_serializer import TagSerializer
from apps.blog.serializers.image_serializer import ImageSerializer
from apps.blog.services.blog_likes import BlogLikeService


class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True, only_fields=['username'], allow_null=True)
    views = serializers.IntegerField(read_only=True)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['slug'] = f"/{instance.slug}"
        rep['tags'] = list(instance.tags.values_list('name', flat=True))
        rep['is_liked_by_user'] = BlogLikeService.has_liked(instance, self.context['request'].user)
        if instance.author is None:
            rep['author'] = None
        return rep

    class Meta:
        model = Blog
        exclude = ['active', 'created_by', 'updated_by']

class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    cover_image = serializers.URLField(required=False, allow_blank=True)
    read_time = serializers.IntegerField(required=False, min_value=0)
    tags = serializers.ListField(child=serializers.CharField(), required=False, write_only=True)
    slug = serializers.CharField(read_only=True)
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['tags'] = list(instance.tags.values_list('name', flat=True))
        return rep

    class Meta:
        model = Blog
        fields = ['title', 'content', 'tags', 'cover_image', 'read_time', 'slug']

    def validate_tags(self, tags=[]):
        validated_tags = []
        tags = [tag.strip().lower() for tag in tags]
        for tag_name in tags:
            tag_obj, created = BlogTag.objects.get_or_create(name=tag_name)
            validated_tags.append(tag_obj)
        return validated_tags

    def create(self, validated_data):
        user = self.context['request'].user
        if not user:
            raise serializers.ValidationError(_("User must be authenticated to create a blog post."))
        validated_data['author'] = user

        tags = validated_data.pop('tags', [])
        validated_data['slug'] = slugify(validated_data['title'])
        try: 
            blog = Blog.objects.create(**validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(_("A blog with this title already exists."))
        
        blog.tags.set(tags)
        return blog

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        title = validated_data.get('title', None)

        if title != instance.title:
            validated_data['slug'] = slugify(title)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if tags is not None:
            instance.tags.set(tags)

        instance.save()
        return instance


class BlogCreateUpdateResponseSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(child=serializers.CharField(), read_only=True)
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'cover_image', 'read_time', 'tags']


class BlogLikeToggleResponseSerializer(serializers.Serializer):
    liked = serializers.BooleanField()
    likes_count = serializers.IntegerField()


