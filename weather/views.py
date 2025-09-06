from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .services import WeatherService
from .models import WeatherAlert, WeatherData
from farms.models import Farm

@login_required
def dashboard(request):
    weather_service = WeatherService()
    user_farms = Farm.objects.filter(owner=request.user)
    weather_data = []
    
    for farm in user_farms:
        if farm.latitude and farm.longitude:
            current_weather = weather_service.get_current_weather(
                float(farm.latitude), 
                float(farm.longitude)
            )
            if current_weather:
                weather_data.append({
                    'farm': farm,
                    'weather': current_weather
                })
    
    alerts = WeatherAlert.objects.filter(is_active=True).order_by('-created_at')
    recent_data = WeatherData.objects.all().order_by('-recorded_at')[:10]
    
    context = {
        'weather_data': weather_data,
        'alerts': alerts,
        'recent_data': recent_data,
    }
    return render(request, 'weather/dashboard.html', context)

@login_required
def get_weather_api(request):
    """API endpoint for AJAX weather requests"""
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if not lat or not lon:
        return JsonResponse({'error': 'Latitude and longitude required'}, status=400)
    
    weather_service = WeatherService()
    current_weather = weather_service.get_current_weather(float(lat), float(lon))
    forecast = weather_service.get_forecast(float(lat), float(lon))
    
    if current_weather:
        weather_service.save_weather_data(current_weather, lat, lon)
        return JsonResponse({
            'current': current_weather,
            'forecast': forecast
        })
    else:
        return JsonResponse({'error': 'Could not fetch weather data'}, status=500)

@login_required
def alerts(request):
    active_alerts = WeatherAlert.objects.filter(is_active=True).order_by('-created_at')
    context = {'alerts': active_alerts}
    return render(request, 'weather/alerts.html', context)