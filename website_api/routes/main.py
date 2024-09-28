import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .swagger import urlpatterns as swagger_urlpatterns

BASE_API_URL = "api/v1"
blog_urls = [
   path('blog/', include('blog.urls')),


]

urlpatterns = (
        [
            path("admin/", admin.site.urls),
            path('__debug__/', include(debug_toolbar.urls)),
            path(f"{BASE_API_URL}/", include("apps.users.routes.api")),
            path(f"{BASE_API_URL}/", include("apps.events.routes.api")),
            path(f"{BASE_API_URL}/", include("apps.events.routes.extra")),
        ] + swagger_urlpatterns
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

handler404 = "apps.users.views.index.page_not_found_view"
handler500 = "apps.users.views.index.server_error_view"
