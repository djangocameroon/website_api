from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import status, serializers
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.events.models.reservation import Reservation
from apps.events.serializers.reservation_serializer import (
    CreateReservationSerializer,
    ReservationSerializer,
)
from mixins.api_response_mixin import APIResponseMixin


class ReservationViewSet(ModelViewSet, APIResponseMixin):
    queryset = Reservation.objects.all()
    authentication_classes = [OAuth2Authentication]
    http_method_names = ["get", "post", "put", "delete"]
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReservationSerializer
        if self.action == "create":
            return CreateReservationSerializer
        return ReservationSerializer

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
        summary="List all reservations",
        operation_id="list_reservations",
        description="List all reservations.",
        tags=["Reservations"],
    )
    def list(self, request, *args, **kwargs):
        reservations = self.get_queryset()
        return self.paginated_response(
            request=request,
            queryset=reservations,
            serializer_class=ReservationSerializer,
            message=_("Reservations listed successfully"),
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Get reservation details",
        operation_id="get_reservation_details",
        description="Get reservation details.",
        tags=["Reservations"],
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Update a reservation",
        operation_id="update_reservation",
        description="Update a reservation.",
        tags=["Reservations"],
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete a reservation",
        operation_id="delete_reservation",
        description="Delete a reservation.",
        tags=["Reservations"],
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

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
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        request.data["user"] = request.user.id

        if serializer.is_valid():
            serializer = CreateReservationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            reservation = Reservation.objects.create(**serializer.validated_data)

            # TODO: Implement the send_email function to send an email to the user

            return self.success(
                message=_("Reservation created successfully"),
                status_code=status.HTTP_201_CREATED,
                data=ReservationSerializer(reservation).data,
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
    @action(detail=False, methods=["POST"], permission_classes=[IsAuthenticated])
    def check_in(self, reservation_id: str) -> Response:
        """
        Check in a reservation.
        """
        try:
            existing_reservation = Reservation.objects.get(id=reservation_id)
        except Reservation.DoesNotExist:
            raise serializers.ValidationError(_("Reservation not found"))

        existing_reservation.check_in = True
        existing_reservation.save()
        return self.success(
            message=_("Reservation checked in successfully"),
            status_code=status.HTTP_200_OK,
        )

    # TODO: Maybe Implement the get_reservations_stats function

    @extend_schema(
        summary="Get reservation statistics",
        operation_id="get_reservations_statistics",
        description="Get reservation statistics.",
        tags=["Reservations"],
    )
    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def get_reservations_statistics(self) -> Response:
        """
        Get reservation statistics.
        """
        pass
