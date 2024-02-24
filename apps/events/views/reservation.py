from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from apps.events.models.reservation import Reservation
from apps.events.serializers.reservation_serializer import (
    CreateReservationInputSerializer,
    CreateReservationSerializer,
    ReservationSerializer,
)
from apps.users.user_permissions import IsConnected, IsOrganizer
from utils.user_utils import get_connected_user


class ReservationViewSet(GenericViewSet):
    permission_classes = [IsConnected]

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CreateReservationInputSerializer,
        url_path="create",
    )
    @swagger_auto_schema(
        operation_summary="Create a reservation for an event.",
        security=[{"Bearer": []}],
        tags=["Reservations"],
        responses={201: ReservationSerializer()},
    )
    def create_reservation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Retrieve the connected user (user making the request)
        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                {"error": "User not connected"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Adding the connected user to the request data
        request.data["user"] = connected_user.id

        # Check if the input data is valid
        if serializer.is_valid():
            # Check if the input data is valid with the new value added
            serializer = CreateReservationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            # TODO: Implement the send_email function to send an email to the user
            # when the reservation is created.

            return Response(
                ReservationSerializer(serializer.instance).data,
                status=status.HTTP_201_CREATED,
            )

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="POST",
    operation_summary="Check in a reservation.",
    security=[{"Bearer": []}],
    tags=["Reservations"],
)
@api_view(["POST"])
@permission_classes([IsOrganizer])
def check_in(request, reservation_id: str) -> Response:
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
@permission_classes([IsOrganizer])
def get_reservations_statistics(request) -> Response:
    """
    Get reservations statistics.
    """
    pass
