from rest_framework import generics
from apps.blog.models.tag import Tag
from apps.blog.serializers.tag_serializer import TagSerializer

class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer