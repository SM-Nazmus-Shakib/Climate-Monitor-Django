from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Farm(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=200)
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    size = models.FloatField(help_text="Size in acres")
    soil_type = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_weather_data(self):
        """Get latest weather data for this farm"""
        return self.weather_data.filter(is_forecast=False).order_by('-recorded_at').first()

class Crop(models.Model):
    CROP_TYPES = [
        ('rice', 'Rice'),
        ('wheat', 'Wheat'),
        ('corn', 'Corn'),
        ('potato', 'Potato'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('other', 'Other'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    crop_type = models.CharField(max_length=50, choices=CROP_TYPES)
    variety = models.CharField(max_length=100)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    current_status = models.CharField(max_length=100, default='Healthy')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_crop_type_display()} ({self.variety}) at {self.farm.name}"