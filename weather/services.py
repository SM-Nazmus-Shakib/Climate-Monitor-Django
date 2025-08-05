import requests
from django.conf import settings
from decimal import Decimal
from .models import WeatherData

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.OPENWEATHER_BASE_URL
    
    def get_current_weather(self, lat, lon):
        """Get current weather data from OpenWeatherMap API"""
        url = f"{self.base_url}/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed'],
                'description': data['weather'][0]['description'],
                'location': data['name']
            }
        except requests.RequestException as e:
            print(f"Weather API error: {e}")
            return None
    
    def get_forecast(self, lat, lon, days=5):
        """Get weather forecast"""
        url = f"{self.base_url}/forecast"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': 'metric'
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            forecast_data = []
            for item in data['list'][:days * 8]:  # 8 forecasts per day (3-hour intervals)
                forecast_data.append({
                    'datetime': item['dt_txt'],
                    'temperature': item['main']['temp'],
                    'humidity': item['main']['humidity'],
                    'description': item['weather'][0]['description'],
                    'wind_speed': item['wind']['speed']
                })
            
            return forecast_data
        except requests.RequestException as e:
            print(f"Forecast API error: {e}")
            return []
    
    def save_weather_data(self, weather_data, lat, lon):
        """Save weather data to database"""
        if weather_data:
            WeatherData.objects.create(
                location=weather_data['location'],
                latitude=Decimal(str(lat)),
                longitude=Decimal(str(lon)),
                temperature=Decimal(str(weather_data['temperature'])),
                humidity=Decimal(str(weather_data['humidity'])),
                pressure=Decimal(str(weather_data['pressure'])),
                wind_speed=Decimal(str(weather_data['wind_speed'])),
                description=weather_data['description']
            )