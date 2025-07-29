
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('groups/', include('groups.urls')),
    path('', include('store.urls')),
    
=======
    path('', include('store.urls')),
>>>>>>> 71ba33cb069cca9059a3f80edd9bc9fe51ae4d8d
]

# To display images
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

