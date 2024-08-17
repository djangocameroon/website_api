from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.events.models.speaker import Speaker
from apps.events.serializers.speaker_serializer import (
    SpeakerSerializer,
    SpeakerWithLastUpdatedBySerializer,
)
from apps.users.permissions.user_permissions import IsOrganizer
from mixins.api_response_mixin import APIResponseMixin
from utils.user_utils import get_connected_user


class SpeakerViewSet(ModelViewSet, APIResponseMixin):
    """
    ViewSet for managing speakers.
    """
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

    def get_permissions(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            permission_classes = [IsOrganizer]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    @extend_schema(
        tags=["Speakers"],
        summary="Create a new speaker",
        operation_id="create_speaker",
        description="Create a new speaker.",
        request=SpeakerWithLastUpdatedBySerializer,
        responses={201: SpeakerWithLastUpdatedBySerializer},
    )
    def create(self, request, *args, **kwargs):
        self._set_connected_user(request)

        serializer = SpeakerWithLastUpdatedBySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return self.success(
            message="Speaker created successfully",
            status_code=status.HTTP_201_CREATED,
            data=serializer.data,
        )

    @extend_schema(
        tags=["Speakers"],
        summary="List all speakers",
        operation_id="list_speakers",
        description="List all speakers.",
        responses={200: SpeakerSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        tags=["Speakers"],
        summary="Get a speaker",
        operation_id="get_speaker",
        description="Get a speaker.",
        responses={200: SpeakerSerializer},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        tags=["Speakers"],
        summary="Update a speaker",
        operation_id="update_speaker",
        description="Update a speaker.",
        request=SpeakerWithLastUpdatedBySerializer,
        responses={200: SpeakerWithLastUpdatedBySerializer},
    )
    def update(self, request, *args, **kwargs):
        self._set_connected_user(request)
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = SpeakerWithLastUpdatedBySerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return self.success(
            message="Speaker updated successfully",
            status_code=status.HTTP_200_OK,
            data=serializer.data,
        )

    @extend_schema(
        tags=["Speakers"],
        summary="Partially update a speaker",
        operation_id="partial_update_speaker",
        description="Partially update a speaker.",
        request=SpeakerWithLastUpdatedBySerializer,
        responses={200: SpeakerWithLastUpdatedBySerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        self._set_connected_user(request)

        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @extend_schema(
        tags=["Speakers"],
        summary="Delete a speaker",
        operation_id="delete_speaker",
        description="Delete a speaker.",
        responses={204: None},
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def _set_connected_user(self, request):
        connected_user = get_connected_user(request)
        if not connected_user:
            return self.error(
                message="User not connected",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        request.data["last_updated_by"] = connected_user.id
        request.data["created_by"] = connected_user.id
        return connected_user
