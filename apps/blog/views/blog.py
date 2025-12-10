from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.blog.models.blog import Blog
from apps.blog.serializers.blog_serializer import BlogSerializer, BlogCreateUpdateSerializer


@extend_schema_view(
    get=extend_schema(
        summary="List blogs",
        description="Retrieve a list of blog posts",
        tags=["Blog"],
        responses={200: BlogSerializer(many=True)},
    ),
    post=extend_schema(
        summary="Create blog",
        description="Create a new blog post",
        tags=["Blog"],
        request=BlogCreateUpdateSerializer,
        responses={201: BlogSerializer},
    ),
)
class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()


@extend_schema_view(
    get=extend_schema(
        summary="Get blog",
        description="Retrieve a blog post",
        tags=["Blog"],
    ),
    put=extend_schema(
        summary="Update blog",
        description="Update a blog post",
        tags=["Blog"],
    ),
    patch=extend_schema(
        summary="Partial update blog",
        description="Partially update a blog post",
        tags=["Blog"],
    ),
    delete=extend_schema(
        summary="Delete blog",
        description="Delete a blog post",
        tags=["Blog"],
        responses={204: None},
    ),
)
class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
