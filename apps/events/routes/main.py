from rest_framework.routers import SimpleRouter

from apps.events.views.event import EventViewSet
from apps.events.views.speaker import SpeakerViewSet


router = SimpleRouter()
router.register(r"speakers", SpeakerViewSet)
router.register(r"events", EventViewSet, basename="events")

urlpatterns = []

urlpatterns += router.urls
