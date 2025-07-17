from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from farms.models import Farm
from .models import WeatherData
import requests
from django.conf import settings
from datetime import datetime, timedelta

@login_required
def weather_dashboard(request):
    farms = Farm.objects.filter(owner=request.user)
    weather_data = WeatherData.objects.filter(farm__in=farms, is_forecast=False).order_by('-recorded_at')[:10]
    
    context = {
        'farms': farms,
        'weather_data': weather_data,
    }
    return render(request, 'weather/dashboard.html', context)

@login_required
def weather_forecast(request, farm_id):
    farm = Farm.objects.get(id=farm_id, owner=request.user)
    
    # In a real app, you would call the weather API's forecast endpoint
    # This is a simplified version
    forecast_data = [
        {
            'date': datetime.now() + timedelta(days=i),
            'temperature': 25 + i,
            'conditions': 'Sunny' if i % 2 == 0 else 'Partly Cloudy',
            'rainfall': 0 if i % 2 == 0 else 5,
        }
        for i in range(1, 6)
    ]
    
    context = {
        'farm': farm,
        'forecast_data': forecast_data,
    }
    return render(request, 'weather/forecast.html', context)

def fetch_weather_data(lat, lon):
    """Fetch current weather data from OpenWeatherMap API"""
    params = {
        'lat': lat,
        'lon': lon,
        'appid': settings.WEATHER_API_KEY,
        'units': 'metric'
    }
    
    try:
        response = requests.get(settings.WEATHER_API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'conditions': data['weather'][0]['main'],
                'rainfall': data.get('rain', {}).get('1h', 0) if 'rain' in data else 0
            }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
    
    return None