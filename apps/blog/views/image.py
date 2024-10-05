from rest_framework import generics
from apps.blog.models.image import Image
from apps.blog.serializers.image_serializer import ImageSerializer
from apps.blog.tasks import handle_image_upload


class ImageListView(generics.ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        handle_image_upload.delay(instance.id)
