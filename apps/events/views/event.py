from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from apps.events.serializers import CreateEventSerializer


class EventViewSet(GenericViewSet):
    @action(
        methods=["POST"],
        detail=False,
        serializer_class=CreateEventSerializer,
        url_path="create-event",
    )
    def create_event(self, request, *args, **kwargs):
        create_event_serializer = CreateEventSerializer(data=request.data)
        if create_event_serializer.is_valid():
            create_event_serializer.save()
            return Response(
                create_event_serializer.data, status=status.HTTP_201_CREATED
            )

        else:
            return Response(
                create_event_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
