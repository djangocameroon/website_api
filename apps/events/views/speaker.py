from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet

from apps.events.models.speaker import Speaker
from apps.events.serializers.speaker_serializer import SpeakerSerializer
from apps.users.user_permissions import IsOrganizer
from utils.user_utils import get_connected_user


@method_decorator(
    name="create",
    decorator=swagger_auto_schema(
        tags=["Speakers"],
        security=[{"Bearer": []}],
        operation_summary="Create a new speaker",
    ),
)
@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        tags=["Speakers"],
        security=[],
        operation_summary="List all speakers",
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        tags=["Speakers"],
        security=[],
        operation_summary="Get a speaker",
    ),
)
@method_decorator(
    name="update",
    decorator=swagger_auto_schema(
        tags=["Speakers"],
        security=[{"Bearer": []}],
        operation_summary="Update a speaker",
    ),
)
@method_decorator(
    name="partial_update",
    decorator=swagger_auto_schema(
        tags=["Speakers"],
        security=[{"Bearer": []}],
        operation_summary="Update a speaker",
    ),
)
@method_decorator(
    name="destroy",
    decorator=swagger_auto_schema(
        tags=["Speakers"],
        security=[{"Bearer": []}],
        operation_summary="Delete a speaker",
    ),
)
class SpeakerViewSet(ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            permission_classes = [IsOrganizer]

        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        self._set_connected_user(request)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self._set_connected_user(request)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        self._set_connected_user(request)
        return super().partial_update(request, *args, **kwargs)

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
