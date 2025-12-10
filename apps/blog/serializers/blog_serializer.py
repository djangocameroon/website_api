from rest_framework import serializers
from apps.blog.models.blog import Blog
from apps.blog.models.author import Author
from apps.blog.models.category import Category
from apps.blog.models.tag import Tag
from apps.blog.serializers.author_serializer import AuthorSerializer
from apps.blog.serializers.category_serializer import CategorySerializer
from apps.blog.serializers.tag_serializer import TagSerializer
from apps.blog.serializers.image_serializer import ImageSerializer


class BlogSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    categories = CategorySerializer(many=True)
    tags = TagSerializer(many=True)
    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = ['author', 'categories', 'tags', 'title', 'content', 'images']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        categories_data = validated_data.pop('categories', [])
        tags_data = validated_data.pop('tags', [])

        author_instance, _ = Author.objects.get_or_create(**author_data)

        blog = Blog.objects.create(author=author_instance, **validated_data)

        self._update_categories_and_tags(blog, categories_data, tags_data)

        return blog

    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        categories_data = validated_data.pop('categories', [])
        tags_data = validated_data.pop('tags', [])

        if author_data:
            author_instance, _ = Author.objects.get_or_create(**author_data)
            instance.author = author_instance

        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()

        self._update_categories_and_tags(instance, categories_data, tags_data)

        return instance

    def _update_categories_and_tags(self, instance, categories_data, tags_data):
        # Update categories
        updated_categories = []
        for category_data in categories_data:
            category, _ = Category.objects.get_or_create(**category_data)
            updated_categories.append(category)
        instance.categories.set(updated_categories)

        # Update tags
        updated_tags = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(**tag_data)
            updated_tags.append(tag)
        instance.tags.set(updated_tags)


class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Blog
        fields = ['author', 'categories', 'tags', 'title', 'content']

    def create(self, validated_data):
        categories = validated_data.pop('categories')
        tags = validated_data.pop('tags')
        blog = Blog.objects.create(**validated_data)
        blog.categories.set(categories)
        blog.tags.set(tags)
        return blog

    def update(self, instance, validated_data):
        categories = validated_data.pop('categories', None)
        tags = validated_data.pop('tags', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if categories is not None:
            instance.categories.set(categories)

        if tags is not None:
            instance.tags.set(tags)

        instance.save()
        return instance
