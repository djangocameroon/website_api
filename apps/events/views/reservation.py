from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.events.models.reservation import Reservation
from apps.events.serializers.reservation_serializer import ReservationInSerializer


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
            # TODO: Implement the send_email function to send an email to the user
            # when the reservation is created.
            return Response(
                {"message": "Reservation created successfully"},
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(
                create_reservation_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
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


# TODO: Maybe Implement the get_reservations_stats function
@api_view(["GET"])
@permission_classes([AllowAny])
def get_reservations_statistics(request) -> Response:
    """
    Get reservations statistics.
    """
    pass
