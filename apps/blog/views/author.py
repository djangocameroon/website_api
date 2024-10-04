from rest_framework import generics
from apps.blog.models.author import Author
from apps.blog.serializers.author_serializer import AuthorSerializer

class AuthorListView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
