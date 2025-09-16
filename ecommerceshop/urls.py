from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('groups/', include('groups.urls')),
    path('', include('store.urls')),
]

# This is the correct way to serve MEDIA files during development.
# The static files are handled automatically by the dev server.
if settings.DEBUG:
    # REMOVE the line for STATIC_URL
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)