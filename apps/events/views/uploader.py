from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.events.serializers.upload_serializer import UploadSerializer
from mixins import APIResponseMixin
from rest_framework.parsers import MultiPartParser

class FileUploadView(APIView, APIResponseMixin):
    """
    View to handle file uploads.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UploadSerializer
    parser_classes = [MultiPartParser]


    @extend_schema(
        operation_id="Upload a file",
        description="Upload a file to the server.",
        tags=["File Upload"],
        request=UploadSerializer,
        responses={201: OpenApiResponse(description="File uploaded successfully")},
    )
    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided'}, status=400)

        file = request.FILES['file']
        file_name = default_storage.save(file.name, ContentFile(file.read()))
        file_url = default_storage.url(file_name)

        return self.success(
            message='File uploaded successfully',
            data={'file_url': file_url},
            status_code=status.HTTP_201_CREATED
        )
