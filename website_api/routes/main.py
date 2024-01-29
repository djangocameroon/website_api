from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Django Cameroon Website API",
        default_version="v1",
        description="Django Cameroon Website API Documentation",
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
    path(
        f"{BASE_API_URL}/users/",
        include(("apps.users.routes", "apps.users")),
        name="users",
    ),
    path(
        f"{BASE_API_URL}/events/",
        include(("apps.events.routes", "apps.events")),
        name="events",
    ),
]
