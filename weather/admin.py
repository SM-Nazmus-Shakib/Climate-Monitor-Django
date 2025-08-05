from django.contrib import admin
from .models import WeatherData, WeatherAlert

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('location', 'temperature', 'humidity', 'recorded_at')
    list_filter = ('recorded_at', 'location')
    search_fields = ('location', 'description')
    readonly_fields = ('recorded_at',)

@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'alert_type', 'severity', 'location', 'is_active', 'start_date')
    list_filter = ('alert_type', 'severity', 'is_active', 'start_date')
    search_fields = ('title', 'location', 'description')
    readonly_fields = ('created_at',)
