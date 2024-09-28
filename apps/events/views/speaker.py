from drf_spectacular.utils import extend_schema
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from apps.events.models.speaker import Speaker
from apps.events.serializers.speaker_serializer import (
    SpeakerSerializer,
    SpeakerWithLastUpdatedBySerializer,
)
from apps.users.serializers.general_serializers import PaginatedResponseSerializer
from mixins.api_response_mixin import APIResponseMixin


class SpeakerViewSet(ModelViewSet, APIResponseMixin):
    """
    ViewSet for managing speakers.
    """
    queryset = Speaker.objects.all()
    authentication_classes = [OAuth2Authentication]
    parser_classes = [JSONParser]
    http_method_names = ["get", "post", "put", "delete"]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return SpeakerSerializer
        return SpeakerWithLastUpdatedBySerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
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
        responses={
            status.HTTP_200_OK: PaginatedResponseSerializer(data_serializer_class=SpeakerSerializer),
        }
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
