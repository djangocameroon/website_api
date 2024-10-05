from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from rest_framework import serializers

from apps.blog.models.post import Post, Tag, Category


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name")

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
        
        
class PostSerializer(serializers.ModelSerializer):
    Category = CategorySerializer()
    Tag = TagSerializer(many =True)
    author = serializers.StringRelatedField
    
    class Meta:
        model = Post
        exclude = ("post_id", "image", "title", "content", "author", "category", "Tag")
        
    def create (self, validated_data):
        category_data = validated_data.pop('category')
        tags_data = validated_data.pop('tag')
        author = self.context['request'].user
        
        category, _ = Category.objects.get_or_create(name = category_data['name'])
        post = Post.objects.create(category = category, author=author, **validated_data)
        
        for tag_data in tags_data:
            tag,_ = Tag.objects.get_or_create(name = tag_data['name'])
            post.tags.add(tag)
            
        return post

