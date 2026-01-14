from django.urls import re_path
from rest_framework.routers import SimpleRouter

from apps.events.views.event import EventViewSet
from apps.events.views.reservation import ReservationViewSet
from apps.events.views.speaker import SpeakerViewSet
from apps.events.views.project import ProjectsListView

router = SimpleRouter()
router.register(r"speakers", SpeakerViewSet)
router.register(r"events", EventViewSet, basename="events")
router.register(r"reservations", ReservationViewSet, basename="reservations")

urlpatterns = router.urls + [
    re_path(r'^projects/$', ProjectsListView.as_view(), name='projects-list'),
]
