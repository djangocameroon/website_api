from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

BASE_API_URL = "api/v1"

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
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
