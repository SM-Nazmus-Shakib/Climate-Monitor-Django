from django.urls import path
from .views import weather_dashboard, weather_forecast

app_name = 'weather'

urlpatterns = [
    path('dashboard/', weather_dashboard, name='dashboard'),
    path('forecast/<int:farm_id>/', weather_forecast, name='forecast'),
]