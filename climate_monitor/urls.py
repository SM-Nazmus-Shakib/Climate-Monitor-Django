from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Include other apps' URLs here
    path('weather/', include('weather.urls')),
    path('farms/', include('farms.urls')),
    path('damage-reports/', include('damage_reports.urls')),
    path('users/', include('users.urls')),
]