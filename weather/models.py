from django.db import models
from farms.models import Farm
from django.contrib.auth import get_user_model

User = get_user_model()

class WeatherData(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_data')
    temperature = models.FloatField()
    humidity = models.FloatField()
    rainfall = models.FloatField()
    wind_speed = models.FloatField()
    pressure = models.FloatField()
    conditions = models.CharField(max_length=100)
    recorded_at = models.DateTimeField(auto_now_add=True)
    is_forecast = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-recorded_at']
        
    def __str__(self):
        return f"{self.farm.name} - {self.recorded_at}"