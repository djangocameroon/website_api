from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from apps.events.models.speaker import Speaker
from apps.events.serializers.speaker_serializer import SpeakerSerializer
from apps.users.user_permissions import IsOrganizer
from utils.user_utils import get_connected_user


class SpeakerViewSet(ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            permission_classes = [IsOrganizer]

        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    @swagger_auto_schema(
        tags=["Speakers"],
        security=[{"Bearer": []}],
        operation_summary="Create a new speaker",
        operation_id="create_speaker",
        operation_description="Create a new speaker.",
    )
    def create(self, request, *args, **kwargs):
        self._set_connected_user(request)
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Speakers"],
        security=[],
        operation_summary="List all speakers",
        operation_id="list_speakers",
        operation_description="List all speakers.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Speakers"],
        security=[],
        operation_summary="Get a speaker",
        operation_id="get_speaker",
        operation_description="Get a speaker.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Speakers"],
        security=[{"Bearer": []}],
        operation_summary="Update a speaker",
        operation_id="update_speaker",
        operation_description="Update a speaker.",
    )
    def update(self, request, *args, **kwargs):
        self._set_connected_user(request)
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Speakers"],
        security=[{"Bearer": []}],
        operation_summary="Update a speaker",
        operation_id="partial_update_speaker",
        operation_description="Update a speaker.",
    )
    def partial_update(self, request, *args, **kwargs):
        self._set_connected_user(request)
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=["Speakers"],
        security=[{"Bearer": []}],
        operation_summary="Delete a speaker",
        operation_id="delete_speaker",
        operation_description="Delete a speaker.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def _set_connected_user(self, request):
        # Retrieve the connected user (user making the request)
        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                {"error": "User not connected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Adding the connected user to the request data
        request.data["last_updated_by"] = connected_user.id
