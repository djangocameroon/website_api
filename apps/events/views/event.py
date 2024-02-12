from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.events.models.event import Event
from apps.events.serializers import CreateEventSerializer, EventSerializer
from apps.events.serializers.reservation_serializer import ReservationSerializer


class EventViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CreateEventSerializer,
        url_path="create",
    )
    def create_event(self, request, *args, **kwargs):
        create_event_serializer = self.get_serializer(data=request.data)
        if create_event_serializer.is_valid():
            create_event_serializer.save()
            return Response(
                create_event_serializer.data,
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
    )
    def get_events(self, request, *args, **kwargs):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([AllowAny])
def publish_event(request, event_id) -> Response:
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


@api_view(["GET"])
@permission_classes([AllowAny])
def get_event_reservations(request, event_id) -> Response:
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
