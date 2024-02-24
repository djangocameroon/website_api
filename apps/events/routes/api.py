from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.events.views.event import (
    EventViewSet,
    publish_event,
    retrieve_event_reservations,
)
from apps.events.views.speaker import SpeakerViewSet


router = SimpleRouter()
router.register(r"speakers", SpeakerViewSet)
router.register(r"events", EventViewSet, basename="events")

urlpatterns = [
    path("events/<str:event_id>/publish/", publish_event),
    path("events/<str:event_id>/reservations/", retrieve_event_reservations),
]

urlpatterns += router.urls
