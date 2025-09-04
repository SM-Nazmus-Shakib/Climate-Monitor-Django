# climate_monitor/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),  
    path("chat/", views.chat_view, name="chat"),  
    path('users/', include('users.urls')),
    path('farms/', include('farms.urls')),
    path('weather/', include('weather.urls')),
    path('damage-reports/', include('damage_reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)