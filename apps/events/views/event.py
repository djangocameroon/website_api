from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.events.models.event import Event
from apps.events.serializers.event_serializer import (
    CreateEventInputSerializer,
    EventSerializer,
)
from apps.events.serializers.reservation_serializer import ReservationSerializer
from mixins.api_response_mixin import APIResponseMixin


class EventViewSet(ModelViewSet, APIResponseMixin):
    queryset = Event.objects.all().select_related('created_by', 'updated_by')
    authentication_classes = [OAuth2Authentication]
    serializer_class = EventSerializer
    http_method_names = ["get", "post", "put", "delete"]
    parser_classes = [JSONParser]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="Create an event",
        operation_id="create_event",
        description="Create an event.",
        request=CreateEventInputSerializer,
        responses={
            201: OpenApiResponse(
                response=EventSerializer(),
                description=_("Event created successfully")
            )
        },
        tags=["Events"],
    )
    def create(self, request, *args, **kwargs):
        create_event_serializer = CreateEventInputSerializer(data=request.data)
        create_event_serializer.is_valid(raise_exception=True)
        event = create_event_serializer.save(created_by=request.user, updated_by=request.user)
        response_serializer = EventSerializer(event)
        return self.success(
            message=_("Event created successfully"),
            status_code=status.HTTP_201_CREATED,
            data=response_serializer.data,
        )

    @extend_schema(
        summary="Get all events",
        operation_id="get_events",
        description="Get all events.",
        responses={
            200: OpenApiResponse(
                response=EventSerializer(many=True),
                description=_("List of events")
            )
        },
        tags=["Events"],
    )
    def list(self, request, *args, **kwargs):
        events = self.get_queryset().select_related(
            'created_by', 'updated_by'
        )
        serializer = EventSerializer(events, many=True)
        return self.success(
            message=_("List of events"),
            status_code=status.HTTP_200_OK,
            data=serializer.data,
        )

    @extend_schema(
        summary="Get event details",
        operation_id="get_event_details",
        description="Get event details.",
        responses={
            200: OpenApiResponse(
                response=EventSerializer,
                description=_("Event details")
            )
        },
        tags=["Events"],
    )
    def retrieve(self, request, *args, **kwargs):
        event = self.get_queryset().select_related(
            'created_by', 'updated_by'
        ).get(pk=kwargs['pk'])
        serializer = EventSerializer(event)
        return self.success(
            message=_("Event details"),
            status_code=status.HTTP_200_OK,
            data=serializer.data,
        )

    @extend_schema(
        summary="Update an event",
        operation_id="update_event",
        description="Update an event.",
        responses={
            200: OpenApiResponse(
                response=EventSerializer,
                description=_("Event updated successfully")
            )
        },
        tags=["Events"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete an event",
        operation_id="delete_event",
        description="Delete an event.",
        responses={204: None},
        tags=["Events"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Publish an event",
        operation_id="publish_event",
        description="Publish an event.",
        responses={
            200: OpenApiResponse(
                description=_("Event published successfully")
            )
        },
        tags=["Events"],
    )
    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def publish_event(self, request, event_id: str) -> Response:
        """
        Publish an event
        """
        try:
            event = Event.objects.only('id').get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError(_("Event not found"))
        event.published = True
        event.save(update_fields=['published'])

        return self.success(
            message=_("Event published successfully"),
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Get all reservations for a specific event",
        operation_id="get_event_reservations",
        description="Get all reservations for a specific event.",
        responses={
            200: OpenApiResponse(
                response=ReservationSerializer(many=True),
                description=_("List of reservations")
            )
        },
        tags=["Events"],
    )
    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def retrieve_event_reservations(self, request, event_id: str) -> Response:
        """
        Get all reservations for a specific event.
        """
        try:
            existing_event = Event.objects.prefetch_related('reservations').get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError(_("Event not found"))

        reservations = existing_event.reservations.only(
            'id', 'user', 'status', 'created_at'
        )
        return self.success(
            message=_("List of reservations"),
            status_code=status.HTTP_200_OK,
            data=ReservationSerializer(reservations, many=True).data,
        )
