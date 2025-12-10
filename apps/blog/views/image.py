from rest_framework import generics
from drf_spectacular.utils import extend_schema, extend_schema_view
from apps.blog.models.image import Image
from apps.blog.serializers.image_serializer import ImageSerializer
from apps.blog.tasks import handle_image_upload


@extend_schema_view(
    get=extend_schema(
        summary="List images",
        description="Retrieve a list of blog images",
        tags=["Blog - Images"],
    ),
    post=extend_schema(
        summary="Create image",
        description="Upload a new blog image",
        tags=["Blog - Images"],
    ),
)
class ImageListView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


@extend_schema(
    summary="Upload image",
    description="Upload a new blog image (async processing)",
    tags=["Blog - Images"],
)
class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        handle_image_upload.delay(instance.id)
