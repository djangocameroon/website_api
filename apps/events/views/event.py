from uuid import UUID

from django.db.models import Q
from django.http import Http404
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.openapi import OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.events.models.event import Event
from apps.events.models.reservation import Reservation
from apps.events.permissions import IsSuperUser
from apps.events.serializers.event_serializer import (
    CreateEventInputSerializer,
    EventSerializer,
)
from apps.events.serializers.reservation_serializer import ReservationSerializer
from apps.users.serializers.general_serializers import PaginationSerializer
from mixins.api_response_mixin import APIResponseMixin


class EventViewSet(ModelViewSet, APIResponseMixin):
    queryset = Event.objects.all().select_related(
        "created_by",
        "updated_by",
        "location",
        "location__city",
        "location__city__region",
    )
    authentication_classes = [OAuth2Authentication]
    http_method_names = ["get", "post", "put", "delete"]
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        return EventSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @extend_schema(
        summary="Get all events",
        operation_id="get_events",
        description="Get all events.",
        parameters=[
            OpenApiParameter(
                name="upcoming",
                location=OpenApiParameter.QUERY,
                description=(
                    "If true, only return published events whose date is in the "
                    "future, ordered soonest first."
                ),
                required=False,
                type=OpenApiTypes.BOOL,
            )
        ],
        responses={
            200: OpenApiResponse(
                response=inline_serializer(
                    name="PaginatedEventListResponse",
                    fields={
                        "status": serializers.BooleanField(),
                        "message": serializers.CharField(),
                        "data": EventSerializer(many=True),
                        "status_code": serializers.IntegerField(default=200),
                        "pagination": PaginationSerializer(),
                    },
                ),
                description=_("List of events"),
            )
        },
        tags=["Events"],
    )
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).order_by("date")
        should_show_unpublished = request.user.is_authenticated and request.user.is_superuser
        if not should_show_unpublished:
            queryset = queryset.filter(published=True)

        page_size_param = request.query_params.get("page_size")
        if page_size_param is None:
            page_size = 10
        else:
            try:
                page_size = int(page_size_param)
            except ValueError:
                raise serializers.ValidationError(_("page_size must be an integer"))

        if request.query_params.get("upcoming", "").lower() in ("1", "true", "yes"):
            queryset = queryset.filter(date__gte=timezone.now())
        return self.paginated_response(
            request=request,
            queryset=queryset,
            page_size=page_size,
            serializer_class=EventSerializer,
            message=_("List of events"),
            status_code=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Create an event",
        operation_id="create_event",
        description="Create an event.",
        request=CreateEventInputSerializer,
        responses={
            201: OpenApiResponse(
                response=EventSerializer, description=_("Event created successfully")
            )
        },
        tags=["Events"],
    )
    def create(self, request, *args, **kwargs):
        create_event_serializer = CreateEventInputSerializer(data=request.data)
        create_event_serializer.is_valid(raise_exception=True)
        event = create_event_serializer.save(
            created_by=request.user, updated_by=request.user
        )
        return self.success(
            message=_("Event created successfully"),
            data=EventSerializer(event).data,
            status_code=status.HTTP_201_CREATED,
        )

    @extend_schema(
        summary="Get event details",
        operation_id="get_event_details",
        description="Get event details.",
        responses={
            200: OpenApiResponse(
                response=EventSerializer, description=_("Event details")
            )
        },
        tags=["Events"],
    )
    def retrieve(self, request, *args, **kwargs):
        lookup_field = self.kwargs.get("pk")
        query = Q(slug=lookup_field)

        try:
            UUID(lookup_field)
            query |= Q(id=lookup_field)
        except ValueError:
            pass

        try:
            event = (
                self.get_queryset()
                .select_related("created_by", "updated_by")
                .get(query)
            )
        except Event.DoesNotExist:
            raise Http404

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
                response=EventSerializer, description=_("Event updated successfully")
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
        responses={200: OpenApiResponse(description=_("Event published successfully"))},
        tags=["Events"],
    )
    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def publish_event(self, request, event_id: str) -> Response:
        """
        Publish an event
        """
        try:
            event = Event.objects.only("id").get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError(_("Event not found"))
        event.published = True
        event.save(update_fields=["published"])

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
                description=_("List of reservations"),
            )
        },
        tags=["Events"],
    )
    @action(detail=False, methods=["GET"], permission_classes=[IsSuperUser])
    def retrieve_event_reservations(self, request) -> Response:
        """
        Get all reservations for a specific event.
        """
        event_id = request.query_params.get("event_id")
        if not event_id:
            raise serializers.ValidationError(_("event_id query parameter is required"))
        try:
            existing_event = Event.objects.only("id").get(id=event_id)
        except Event.DoesNotExist:
            raise serializers.ValidationError(_("Event not found"))

        reservations = existing_event.reservations.select_related("user", "for_event")
        return self.success(
            message=_("List of reservations"),
            status_code=status.HTTP_200_OK,
            data=ReservationSerializer(reservations, many=True).data,
        )

    @extend_schema(
        summary="Check if the current user has registered for an event",
        operation_id="check_event_registration",
        description="Check whether the authenticated user has an existing reservation for the given event.",
        responses={200: OpenApiResponse(description=_("Registration status"))},
        tags=["Events"],
    )
    @action(detail=False, methods=["GET"], permission_classes=[IsAuthenticated])
    def check_registration(self, request) -> Response:
        """
        Check if the current authenticated user has registered for an event.
        """
        event_id = request.query_params.get("event_id")
        if not event_id:
            raise serializers.ValidationError(_("event_id query parameter is required"))

        reservation = (
            Reservation.objects.filter(for_event_id=event_id, user=request.user)
            .only("id")
            .first()
        )

        return self.success(
            message=_("Registration status"),
            status_code=status.HTTP_200_OK,
            data={
                "registered": reservation is not None,
                "reservation_id": reservation.id if reservation else None,
            },
        )
