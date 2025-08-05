from django.contrib import admin
from .models import Farm, CropMonitoring

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'crop_type', 'area_acres', 'planting_date')
    list_filter = ('crop_type', 'planting_date', 'created_at')
    search_fields = ('name', 'location', 'owner__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('owner', 'name', 'location')
        }),
        ('Geographic Details', {
            'fields': ('latitude', 'longitude', 'area_acres')
        }),
        ('Crop Information', {
            'fields': ('crop_type', 'planting_date', 'expected_harvest_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(CropMonitoring)
class CropMonitoringAdmin(admin.ModelAdmin):
    list_display = ('farm', 'health_status', 'recorded_at')
    list_filter = ('health_status', 'recorded_at')
    search_fields = ('farm__name', 'notes')
    readonly_fields = ('recorded_at',)