from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import SimpleRouter

from utils.main import load_documentation
from apps.events.views import (
    EventViewSet,
    SpeakerViewSet, 
    ReservationViewSet,
    get_event_reservations,
    check_in,
    publish_event,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Django Cameroon Website API",
        default_version="v1",
        description=load_documentation("main.md"),
        terms_of_service="https://djangocameroon.site/",
        contact=openapi.Contact(email="support@djangocameroon.site"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

BASE_API_URL = "api/v1"

event_router = SimpleRouter(trailing_slash=False)
event_router.register("", EventViewSet, basename="events")

speaker_router = SimpleRouter(trailing_slash=False)
speaker_router.register("", SpeakerViewSet, basename="speakers")

reservation_router = SimpleRouter(trailing_slash=False)
reservation_router.register("", ReservationViewSet, basename="reservations")

urlpatterns = (
    [
        re_path(
            r"^$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
        ),
        path(
            "swagger<format>/",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path("admin/", admin.site.urls),
        # path(
        #     f"{BASE_API_URL}/users/",
        #     include(("apps.users.routes", "apps.users")),
        #     name="users",
        # ),
        # path(
        #     f"{BASE_API_URL}/events/",
        #     include(("apps.events.routes", "apps.events")),
        #     name="events",
        # ),
        path(f"{BASE_API_URL}/events/", include(event_router.urls), name="events"),
        path(
            f"{BASE_API_URL}/events/<int:event_id>/publish",
            publish_event,
            name="publish_event",
        ),
        path(
            f"{BASE_API_URL}/speakers/",
            include(speaker_router.urls),
            name="speakers",
        ),
        path(
            f"{BASE_API_URL}/reservations/",
            include(reservation_router.urls),
            name="reservations",
        ),
        path(
            f"{BASE_API_URL}/reservations/event/<int:event_id>",
            get_event_reservations,
            name="event_reservations",
        ),
        path(
            f"{BASE_API_URL}/reservations/<int:reservation_id>/check-in",
            check_in,
            name="reservation_check_in",
        ),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
