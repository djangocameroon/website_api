from django.contrib import admin
from django.urls import path, re_path, include
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

urlpatterns = [
    re_path(r"^$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),

    # Users app
    path("api/",include('apps.users.routes.api')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(
    settings.STATIC_URL, document_root=settings.STATIC_ROOT
)
