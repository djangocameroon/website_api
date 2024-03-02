from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.events.models.event import Event
from apps.events.serializers.event_serializer import (
    CreateEventInputSerializer,
    CreateEventSerializer,
    EventSerializer,
)
from apps.events.serializers.reservation_serializer import ReservationSerializer
from apps.users.user_permissions import IsOrganizer
from utils.user_utils import get_connected_user


class EventViewSet(GenericViewSet):

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CreateEventInputSerializer,
        url_path="create",
        permission_classes=[IsOrganizer],
    )
    @swagger_auto_schema(
        operation_summary="Create an event",
        operation_id="create_event",
        operation_description="Create an event.",
        responses={201: EventSerializer()},
        security=[{"Bearer": []}],
        tags=["Events"],
    )
    def create_event(self, request, *args, **kwargs):
        create_event_serializer = self.get_serializer(data=request.data)

        # Retrieve the connected user (user making the request)
        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                {"error": "User not connected"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Adding the connected user to the request data
        request.data["created_by"] = connected_user.id

        # Check if the input data is valid
        if create_event_serializer.is_valid():
            # Check if the input data is valid with the new value added
            create_event_serializer = CreateEventSerializer(data=request.data)
            create_event_serializer.is_valid(raise_exception=True)
            
            create_event_serializer.save()
            return Response(
                EventSerializer(create_event_serializer.instance).data,
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                create_event_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=["GET"],
        detail=False,
        url_path="list",
        serializer_class=EventSerializer,
        permission_classes=[AllowAny],
    )
    @swagger_auto_schema(
        operation_summary="Get all events",
        operation_id="get_events",
        operation_description="Get all events.",
        responses={200: EventSerializer(many=True)},
        security=[],
        tags=["Events"],
    )
    def get_events(self, request, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="POST",
    operation_summary="Publish an event",
    operation_id="publish_event",
    operation_description="Publish an event.",
    security=[{"Bearer": []}],
    tags=["Events"],
)
@api_view(["POST"])
@permission_classes([IsOrganizer])
def publish_event(request, event_id: str) -> Response:
    """
    Publish an event
    """
    try:
        event = Event.objects.get(id=event_id)
    except:
        event = None

    if not event:
        return Response(
            {"error": "Event not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    event.published = True
    event.save()

    # TODO: Implement the send_email function to send an email to the
    # community members
    return Response(
        {"message": "Event published successfully"},
        status=status.HTTP_200_OK,
    )


@swagger_auto_schema(
    method="GET",
    operation_summary="Get all reservations for a specific event",
    operation_id="get_event_reservations",
    operation_description="Get all reservations for a specific event.",
    responses={200: ReservationSerializer(many=True)},
    security=[{"Bearer": []}],
    tags=["Events"],
)
@api_view(["GET"])
@permission_classes([IsOrganizer])
def retrieve_event_reservations(request, event_id: str) -> Response:
    """
    Get all reservations for a specific event.
    """
    try:
        existing_event = Event.objects.get(id=event_id)
    except:
        existing_event = None

    if not existing_event:
        return Response(
            {"error": "Event not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    reservations = existing_event.reservations.all()
    return Response(
        ReservationSerializer(reservations, many=True).data,
        status=status.HTTP_200_OK,
    )
