from django.urls import path
from . import views

app_name = 'weather'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('alerts/', views.alerts, name='alerts'),
    path('api/weather/', views.get_weather_api, name='weather_api'),
]