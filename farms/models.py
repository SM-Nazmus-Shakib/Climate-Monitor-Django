from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Farm(models.Model):
    CROP_CHOICES = [
        ('rice', 'Rice'),
        ('wheat', 'Wheat'),
        ('corn', 'Corn'),
        ('potato', 'Potato'),
        ('tomato', 'Tomato'),
        ('onion', 'Onion'),
        ('other', 'Other'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    area_acres = models.DecimalField(max_digits=10, decimal_places=2)
    crop_type = models.CharField(max_length=20, choices=CROP_CHOICES)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.owner.username}"

class CropMonitoring(models.Model):
    HEALTH_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
        ('critical', 'Critical'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='monitoring_records')
    health_status = models.CharField(max_length=20, choices=HEALTH_CHOICES)
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.farm.name} - {self.health_status} - {self.recorded_at.date()}"
