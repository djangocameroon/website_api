from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from apps.events.models.event import Event
from apps.events.serializers import CreateEventSerializer, EventSerializer


class EventViewSet(GenericViewSet):
    permission_classes = [AllowAny]

    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CreateEventSerializer,
        url_path="create-event",
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
