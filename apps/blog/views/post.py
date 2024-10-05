from rest_framework import generics, permissions
from apps.blog.models.blog import Blog
from apps.blog.serializers.blog_serializer import  BlogSerializer, BlogCreateUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


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

    @swagger_auto_schema(
        operation_description="Retrieve a list of blog posts",
        responses={200: BlogSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new blog post",
        request_body=BlogCreateUpdateSerializer,
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

    @swagger_auto_schema(
        operation_description="Retrieve a blog post",
        responses={200: BlogSerializer}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a blog post",
        request_body=BlogCreateUpdateSerializer,
        responses={200: BlogSerializer}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a blog post",
        responses={204: openapi.Response(description="No Content")}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
