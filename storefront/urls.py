from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

admin.site.site_header = "Storefront Admin"
admin.site.index_title = "Admin"


urlpatterns = [
    path("", include("core.urls")),
    path("admin/", admin.site.urls),
    path("playground/", include("playground.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
    path("store/", include("store.urls")),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
