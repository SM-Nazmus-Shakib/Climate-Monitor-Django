from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', include('weather.urls')),
    path('farms/', include('farms.urls')),
    path('damage-reports/', include('damage_reports.urls')),
    path('users/', include('users.urls')),
    path('', include('farms.urls')),  # Default to farms map
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)