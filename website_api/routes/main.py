from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static

from utils.main import load_documentation

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
        # Users app
        path(f"{BASE_API_URL}/", include("apps.users.routes.api")),
        # Events app
        path(f"{BASE_API_URL}/", include("apps.events.routes.api")),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)
