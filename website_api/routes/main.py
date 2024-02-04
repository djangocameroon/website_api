from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from utils.main import load_documentation

from apps.events.views.event import EventViewSet
from rest_framework.routers import SimpleRouter

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

event_router = SimpleRouter()
event_router.register("", EventViewSet, basename="events")

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
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
