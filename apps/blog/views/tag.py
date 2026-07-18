from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.blog.models.tag import BlogTag
from apps.blog.serializers.tag_serializer import TagSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List tags",
        description="Retrieve a list of blog tags",
        tags=["Blog - Tags"],
    ),
    post=extend_schema(
        summary="Create tag",
        description="Create a new blog tag",
        tags=["Blog - Tags"],
    ),
)
class TagListView(generics.ListCreateAPIView):
    queryset = BlogTag.objects.all()
    serializer_class = TagSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
