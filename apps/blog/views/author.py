from rest_framework import generics
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.blog.models.author import Author
from apps.blog.serializers.author_serializer import AuthorSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List authors",
        description="Retrieve a list of blog authors",
        tags=["Blog - Authors"],
    ),
    post=extend_schema(
        summary="Create author",
        description="Create a new blog author",
        tags=["Blog - Authors"],
    ),
)
class AuthorListView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
