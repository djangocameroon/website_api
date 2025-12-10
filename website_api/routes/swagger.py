from django.conf import settings
from django.urls import path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.views.generic import TemplateView
from apps.users.views.index import index

urlpatterns = [
    path('', index, name='index'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', TemplateView.as_view(template_name='docs/redoc.html'), name='index'),
]

from django.conf import settings
from django.urls import path, re_path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.views.generic import TemplateView
from apps.users.views.index import index

if settings.ENVIRONMENT == "development":
    urlpatterns = [
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('', TemplateView.as_view(template_name='docs/redoc.html'), name='index'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        # re_path(r'^$', TemplateView.as_view(template_name='docs/redoc.html'), name='index'),
        # re_path(r'$swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
elif settings.ENVIRONMENT == "production":
    urlpatterns = [
        path('', index, name='index'),
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', TemplateView.as_view(template_name='docs/redoc.html'), name='index'),
    ]
