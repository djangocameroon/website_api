from django.conf import settings
from django.urls import path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.users.views.index import index

if settings.ENVIRONMENT == "development":
    urlpatterns = [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        re_path(r'$', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
elif settings.ENVIRONMENT == "production":
    urlpatterns = [
        path('', index, name='index'),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
