from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.events.models.event import Event
from apps.events.models.reservation import Reservation
from apps.events.serializers.reservation_serializer import (
    ReservationInSerializer,
    ReservationSerializer,
)


class ReservationViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=ReservationInSerializer,
        url_path="create",
    )
    def create_reservation(self, request, *args, **kwargs):
        create_reservation_serializer = self.get_serializer(data=request.data)
        if create_reservation_serializer.is_valid():
            create_reservation_serializer.save()
            return Response(
                {"message": "Reservation created successfully"},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                create_reservation_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
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

    reservations = Reservation.objects.filter(event=existing_event)
    return Response(
        ReservationSerializer(reservations, many=True).data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def check_in(request, reservation_id) -> Response:
    """
    Check in a reservation.
    """
    try:
        existing_reservation = Reservation.objects.get(id=reservation_id)
    except:
        existing_reservation = None

    if not existing_reservation:
        return Response(
            {"error": "Reservation not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    existing_reservation.check_in = True
    existing_reservation.save()

    return Response(
        {"message": "Reservation checked in successfully"},
        status=status.HTTP_200_OK,
    )
