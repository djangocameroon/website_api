from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import permissions
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from apps.events.models import Project
from apps.events.serializers.project_serializer import ProjectSerializer
from mixins import APIResponseMixin


class ProjectsListView(APIResponseMixin, APIView):
    permission_classes = (permissions.AllowAny,)
    parser_classes = [JSONParser]

    @extend_schema(
        operation_id="List projects",
        summary="Get list of all published projects",
        tags=["Projects"],
        responses={
            200: OpenApiResponse(
                response=ProjectSerializer(many=True),
                description=_("Projects retrieved successfully")
            ),
        }
    )
    def get(self, request):
        projects = Project.objects.filter(published=True).order_by('-is_featured', '-created_at')
        serializer = ProjectSerializer(projects, many=True)
        return self.success(
            message=_('Projects retrieved successfully'),
            status_code=status.HTTP_200_OK,
            data=serializer.data,
        )
