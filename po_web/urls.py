from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# path('@', include('website.urls')),
urlpatterns = [
    path('@', include('feedback.urls')),
    path('webhooks/', include('webhooks.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('extensions.urls')),
    path('', include('dashboard.urls')),

    # Автообновлние
    path('__reload__/', include('django_browser_reload.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
