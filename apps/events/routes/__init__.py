from rest_framework.routers import SimpleRouter

from apps.events.views.event import EventViewSet


router = SimpleRouter()
router.register(EventViewSet, basename="events")

urlpatterns = []

urlpatterns += router.urls
