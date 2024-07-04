from rest_framework import serializers
from .models import Tag, Category, Author, Blog, Image

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'name', 'bio')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

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

     
        if categories_data:
            categories_instances = [
                Category.objects.get_or_create(**category_data)[0]
                for category_data in categories_data
            ]
            blog.categories.add(*categories_instances)

      
        if tags_data:
            tags_instances = [
                Tag.objects.get_or_create(**tag_data)[0]
                for tag_data in tags_data
            ]
            blog.tags.add(*tags_instances)

        return blog

class BlogCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'

