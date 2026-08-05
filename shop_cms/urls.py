from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# Non-translated URLs (language switch endpoint, theme toggle, admin, QR image)
urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
    path("theme/toggle/", include("core.theme_urls")),
]

# Translated URLs -> every page is reachable as /fa/... or /en/...
urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("products.urls")),
    prefix_default_language=True,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
