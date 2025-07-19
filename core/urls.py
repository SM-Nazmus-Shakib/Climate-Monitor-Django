from django.urls import path
from .views import home, no_permission, climate_dashboard

app_name = 'core'  

urlpatterns = [
    path('', home, name='home'),
    path('no-permission/', no_permission, name='no-permission'),
    path('dashboard/', climate_dashboard, name='climate-dashboard'),
]