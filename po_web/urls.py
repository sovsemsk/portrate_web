from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("@", include("feedback.urls")),
    path("webhooks/", include("webhooks.urls")),
    path("widget/", include("widget.urls")),
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),

    #
    path("i18n/", include('django.conf.urls.i18n')),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
