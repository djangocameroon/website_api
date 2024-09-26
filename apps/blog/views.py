from rest_framework import generics, permissions
from .models.models import Blog, Tag, Category, Author, Image
from .serializers import BlogSerializer, BlogCreateUpdateSerializer, TagSerializer, CategorySerializer, AuthorSerializer, ImageSerializer

from .serializers import BlogSerializer, BlogCreateUpdateSerializer, TagSerializer, CategorySerializer, AuthorSerializer, ImageSerializer


from .tasks import handle_image_upload
from django.http import HttpResponse
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

class TagListView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class AuthorListView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class ImageListView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        handle_image_upload.delay(instance.id)

class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogCreateUpdateSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [permissions.IsAuthenticated]
        return super().get_permissions()

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

def index(request):
    return HttpResponse("Hello, world! This is the django cameroon page.")
