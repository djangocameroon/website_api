from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.events.models.reservation import Reservation
from apps.events.serializers.reservation_serializer import (
    CreateReservationInputSerializer,
    CreateReservationSerializer,
    ReservationSerializer,
)
from mixins.api_response_mixin import APIResponseMixin
from utils.user_utils import get_connected_user


class ReservationViewSet(GenericViewSet, APIResponseMixin):
    queryset = Reservation.objects.all()
    permission_classes = []

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CreateReservationInputSerializer,
        url_path="create",
    )
    @extend_schema(
        summary="Create a reservation for an event.",
        operation_id="create_reservation",
        description="Create a reservation for an event.",
        tags=["Reservations"],
        responses={
            201: OpenApiResponse(
                response=ReservationSerializer,
                description=_("Reservation created successfully")
            )
        },
    )
    def create_reservation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        connected_user = get_connected_user(request)
        if not connected_user:
            return self.error(
                message=_("User not connected"),
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=["User not connected"],
            )
        request.data["user"] = connected_user.id

        if serializer.is_valid():
            serializer = CreateReservationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            reservation = Reservation.objects.create(**serializer.validated_data)

            # TODO: Implement the send_email function to send an email to the user

            return Response(
                ReservationSerializer(reservation).data,
                status=status.HTTP_201_CREATED,
            )

        else:
            return self.error(
                message=_("Validation error"),
                status_code=status.HTTP_400_BAD_REQUEST,
                errors=serializer.errors,
            )

    @extend_schema(
        summary="Check in a reservation.",
        operation_id="check_in_reservation",
        description="Check in a reservation.",
        tags=["Reservations"],
        responses={
            200: OpenApiResponse(
                description=_("Reservation checked in successfully")
            )
        },
    )
    @api_view(["POST"])
    def check_in(self, reservation_id: str) -> Response:
        """
        Check in a reservation.
        """
        try:
            existing_reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            return Response(
                {"error": _("Reservation not found")},
                status=status.HTTP_404_NOT_FOUND,
            )

        existing_reservation.check_in = True
        existing_reservation.save()

        return self.success(
            message=_("Reservation checked in successfully"),
            status_code=status.HTTP_200_OK,
        )

    # TODO: Maybe Implement the get_reservations_stats function
    @api_view(["GET"])
    def get_reservations_statistics(request) -> Response:
        """
        Get reservation statistics.
        """
        pass
