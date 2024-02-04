from rest_framework.routers import DefaultRouter

from apps.events.views.event import EventViewSet


router = DefaultRouter()
router.register("", EventViewSet, basename="events")

urlpatterns = []

urlpatterns += router.urls
