from rest_framework import generics, permissions
from drf_spectacular.utils import extend_schema
from apps.blog.models.blog import Blog
from apps.blog.serializers.blog_serializer import BlogSerializer, BlogCreateUpdateSerializer


class PostList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogCreateUpdateSerializer
        return BlogSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

    @extend_schema(
        summary="List blog posts",
        description="Retrieve a list of blog posts",
        tags=["Blog"],
        responses={200: BlogSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Create blog post",
        description="Create a new blog post",
        tags=["Blog"],
        request=BlogCreateUpdateSerializer,
        responses={201: BlogSerializer}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BlogCreateUpdateSerializer
        return BlogSerializer

    @extend_schema(
        summary="Get blog post",
        description="Retrieve a blog post",
        tags=["Blog"],
        responses={200: BlogSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Update blog post",
        description="Update a blog post",
        tags=["Blog"],
        request=BlogCreateUpdateSerializer,
        responses={200: BlogSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        summary="Delete blog post",
        description="Delete a blog post",
        tags=["Blog"],
        responses={204: None}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
