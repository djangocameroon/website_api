from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.events.models.event import Event
from apps.events.serializers.event_serializer import (
    CreateEventInputSerializer,
    CreateEventSerializer,
    EventSerializer,
)
from apps.events.serializers.reservation_serializer import ReservationSerializer
from apps.users.permissions.user_permissions import IsOrganizer
from mixins.api_response_mixin import APIResponseMixin
from utils.user_utils import get_connected_user


class EventViewSet(GenericViewSet, APIResponseMixin):
    queryset = Event.objects.all()

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CreateEventInputSerializer,
        url_path="create",
        permission_classes=[IsOrganizer],
    )
    @extend_schema(
        summary="Create an event",
        operation_id="create_event",
        description="Create an event.",
        responses={
            201: OpenApiResponse(
                response=EventSerializer,
                description=_("Event created successfully")
            )
        },
        tags=["Events"],
    )
    def create_event(self, request, *args, **kwargs):
        create_event_serializer = self.get_serializer(data=request.data)

        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                {"error": "User not connected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["created_by"] = connected_user.id

        if create_event_serializer.is_valid():
            create_event_serializer = CreateEventSerializer(data=request.data)
            create_event_serializer.is_valid(raise_exception=True)

            create_event_serializer.save()
            return Response(
                EventSerializer(create_event_serializer.instance).data,
                status=status.HTTP_201_CREATED,
            )

        else:
            return self.error(
                message=_("Error creating event"),
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=create_event_serializer.errors,
            )

    @action(
        methods=["GET"],
        detail=False,
        url_path="list",
        serializer_class=EventSerializer,
        permission_classes=[AllowAny],
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
    def get_events(self, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return self.success(
            message=_("List of events"),
            status_code=status.HTTP_200_OK,
            data=serializer.data,
        )

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
    @api_view(["POST"])
    @permission_classes([IsOrganizer])
    def publish_event(self, event_id: str) -> Response:
        """
        Publish an event
        """
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return self.error(
                message=_("Event not found"),
                status_code=status.HTTP_404_NOT_FOUND,
            )

        event.published = True
        event.save()

        # TODO: Implement the send_email function to send an email to the
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
    @api_view(["GET"])
    @permission_classes([IsOrganizer])
    def retrieve_event_reservations(self, event_id: str) -> Response:
        """
        Get all reservations for a specific event.
        """
        try:
            existing_event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return self.error(
                message=_("Event not found"),
                status_code=status.HTTP_404_NOT_FOUND,
            )

        reservations = existing_event.reservations.all()
        return self.success(
            message=_("List of reservations"),
            status_code=status.HTTP_200_OK,
            data=ReservationSerializer(reservations, many=True).data,
        )
