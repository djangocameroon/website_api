from django.urls import path
from rest_framework.routers import SimpleRouter

from apps.events.views.event import (
    EventViewSet,
    publish_event,
    retrieve_event_reservations,
)
from apps.events.views.reservation import ReservationViewSet, check_in
from apps.events.views.speaker import SpeakerViewSet


router = SimpleRouter()
router.register(r"speakers", SpeakerViewSet)
router.register(r"events", EventViewSet, basename="events")
router.register(r"reservations", ReservationViewSet, basename="reservations")

urlpatterns = [
    path("events/<str:event_id>/publish/", publish_event),
    path("events/<str:event_id>/reservations/", retrieve_event_reservations),
    path("reservations/<str:reservation_id>/check-in/", check_in),
]

urlpatterns += router.urls
