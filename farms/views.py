from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Avg, Count
from django.utils import timezone
from datetime import datetime, timedelta
import requests
import json
from .models import Farm, CropMonitoring
from .forms import FarmForm, CropMonitoringForm

@login_required
def dashboard(request):
    farms = Farm.objects.filter(owner=request.user).select_related('owner')
    monitoring_records = CropMonitoring.objects.filter(farm__owner=request.user)
    
    # Calculate statistics
    total_area = farms.aggregate(total=Sum('area_acres'))['total'] or 0
    recent_monitoring = monitoring_records.filter(
        recorded_at__gte=timezone.now() - timedelta(days=7)
    ).count()
    
    # Get farms with coordinates for map
    farms_with_coords = farms.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    )
    
    context = {
        'farms': farms[:6],  # Show only recent 6 farms on dashboard
        'farms_with_coords': farms_with_coords,
        'total_farms': farms.count(),
        'total_area': round(total_area, 2),
        'recent_monitoring': recent_monitoring,
        'health_summary': get_health_summary(request.user),
    }
    return render(request, 'farms/dashboard.html', context)

@login_required
def farm_list(request):
    farms = Farm.objects.filter(owner=request.user).order_by('-created_at')
    
    # Filter by crop type if provided
    crop_filter = request.GET.get('crop_type')
    if crop_filter:
        farms = farms.filter(crop_type=crop_filter)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        farms = farms.filter(
            name__icontains=search
        ) or farms.filter(
            location__icontains=search
        )
    
    context = {
        'farms': farms,
        'crop_types': Farm.CROP_CHOICES,
        'current_crop_filter': crop_filter,
        'current_search': search,
    }
    return render(request, 'farms/farm_list.html', context)

@login_required
def farm_detail(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, owner=request.user)
    monitoring_records = CropMonitoring.objects.filter(farm=farm).order_by('-recorded_at')
    
    # Handle monitoring form submission
    if request.method == 'POST':
        form = CropMonitoringForm(request.POST)
        if form.is_valid():
            monitoring = form.save(commit=False)
            monitoring.farm = farm
            monitoring.save()
            messages.success(request, 'Crop monitoring record added successfully!')
            return redirect('farms:farm_detail', farm_id=farm.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CropMonitoringForm()
    
    # Calculate farm statistics
    planting_date = farm.planting_date
    harvest_date = farm.expected_harvest_date
    today = timezone.now().date()
    
    days_since_planting = (today - planting_date).days if planting_date <= today else 0
    days_to_harvest = (harvest_date - today).days if harvest_date > today else 0
    total_growth_period = (harvest_date - planting_date).days
    growth_progress = min(100, max(0, (days_since_planting / total_growth_period) * 100)) if total_growth_period > 0 else 0
    
    # Get weather data if coordinates exist
    weather_data = None
    if farm.latitude and farm.longitude:
        weather_data = get_weather_data(float(farm.latitude), float(farm.longitude))
    
    context = {
        'farm': farm,
        'monitoring_records': monitoring_records,
        'form': form,
        'days_since_planting': days_since_planting,
        'days_to_harvest': days_to_harvest,
        'growth_progress': round(growth_progress, 1),
        'weather_data': weather_data,
        'recent_monitoring': monitoring_records[:5],  # Last 5 records
    }
    return render(request, 'farms/farm_detail.html', context)

@login_required
def farm_create(request):
    if request.method == 'POST':
        form = FarmForm(request.POST)
        if form.is_valid():
            farm = form.save(commit=False)
            farm.owner = request.user
            farm.save()
            messages.success(request, f'Farm "{farm.name}" added successfully!')
            
            # Log the creation
            CropMonitoring.objects.create(
                farm=farm,
                health_status='good',
                notes=f'Farm "{farm.name}" created and registered in the system.'
            )
            
            return redirect('farms:farm_detail', farm_id=farm.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FarmForm()
    
    context = {
        'form': form, 
        'title': 'Add New Farm',
        'action': 'create'
    }
    return render(request, 'farms/farm_form.html', context)

@login_required
def farm_edit(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, owner=request.user)
    
    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            updated_farm = form.save()
            messages.success(request, f'Farm "{updated_farm.name}" updated successfully!')
            
            # Log the update
            CropMonitoring.objects.create(
                farm=updated_farm,
                health_status='good',
                notes=f'Farm details updated: {", ".join([f.name for f in form.changed_data])}'
            )
            
            return redirect('farms:farm_detail', farm_id=updated_farm.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FarmForm(instance=farm)
    
    context = {
        'form': form, 
        'title': 'Edit Farm',
        'farm': farm,
        'action': 'edit'
    }
    return render(request, 'farms/farm_form.html', context)

@login_required
@require_http_methods(["DELETE"])
def farm_delete(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, owner=request.user)
    farm_name = farm.name
    farm.delete()
    messages.success(request, f'Farm "{farm_name}" deleted successfully!')
    return JsonResponse({'success': True})

@login_required
def weather_api(request):
    """API endpoint to get weather data for farm coordinates"""
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if not lat or not lon:
        return JsonResponse({'error': 'Latitude and longitude required'}, status=400)
    
    try:
        weather_data = get_weather_data(float(lat), float(lon))
        return JsonResponse(weather_data)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def farm_analytics(request, farm_id):
    """Get analytics data for a specific farm"""
    farm = get_object_or_404(Farm, id=farm_id, owner=request.user)
    
    # Get monitoring history
    monitoring_records = CropMonitoring.objects.filter(farm=farm).order_by('recorded_at')
    
    # Prepare data for charts
    monitoring_data = []
    for record in monitoring_records:
        monitoring_data.append({
            'date': record.recorded_at.strftime('%Y-%m-%d'),
            'health_status': record.health_status,
            'health_score': get_health_score(record.health_status),
        })
    
    # Calculate health trends
    recent_records = monitoring_records.filter(
        recorded_at__gte=timezone.now() - timedelta(days=30)
    )
    
    health_distribution = {}
    for choice_value, choice_display in CropMonitoring.HEALTH_CHOICES:
        count = recent_records.filter(health_status=choice_value).count()
        health_distribution[choice_display] = count
    
    return JsonResponse({
        'monitoring_timeline': monitoring_data,
        'health_distribution': health_distribution,
        'total_records': monitoring_records.count(),
        'farm_age_days': (timezone.now().date() - farm.planting_date).days,
    })

@login_required
def export_farm_data(request, farm_id):
    """Export farm data as JSON"""
    farm = get_object_or_404(Farm, id=farm_id, owner=request.user)
    monitoring_records = CropMonitoring.objects.filter(farm=farm).order_by('recorded_at')
    
    export_data = {
        'farm_info': {
            'name': farm.name,
            'location': farm.location,
            'coordinates': {
                'latitude': float(farm.latitude) if farm.latitude else None,
                'longitude': float(farm.longitude) if farm.longitude else None,
            },
            'area_acres': float(farm.area_acres),
            'crop_type': farm.crop_type,
            'planting_date': farm.planting_date.isoformat(),
            'expected_harvest_date': farm.expected_harvest_date.isoformat(),
            'created_at': farm.created_at.isoformat(),
        },
        'monitoring_records': [
            {
                'date': record.recorded_at.isoformat(),
                'health_status': record.health_status,
                'health_display': record.get_health_status_display(),
                'notes': record.notes,
            }
            for record in monitoring_records
        ],
        'export_metadata': {
            'export_date': timezone.now().isoformat(),
            'total_records': monitoring_records.count(),
            'user': request.user.username,
        }
    }
    
    response = JsonResponse(export_data, json_dumps_params={'indent': 2})
    response['Content-Disposition'] = f'attachment; filename="{farm.name}_export.json"'
    return response

# Helper functions

def get_health_summary(user):
    """Get overall health summary for user's farms"""
    monitoring_records = CropMonitoring.objects.filter(
        farm__owner=user,
        recorded_at__gte=timezone.now() - timedelta(days=7)
    )
    
    if not monitoring_records.exists():
        return {'status': 'no_data', 'message': 'No recent monitoring data'}
    
    health_counts = {}
    for choice_value, choice_display in CropMonitoring.HEALTH_CHOICES:
        health_counts[choice_value] = monitoring_records.filter(health_status=choice_value).count()
    
    total_records = sum(health_counts.values())
    
    # Determine overall status
    if health_counts.get('critical', 0) > 0:
        status = 'critical'
        message = f"{health_counts['critical']} farms need immediate attention"
    elif health_counts.get('poor', 0) > 0:
        status = 'poor'
        message = f"{health_counts['poor']} farms need attention"
    elif health_counts.get('fair', 0) > total_records * 0.5:
        status = 'fair'
        message = "Most farms are doing okay"
    else:
        status = 'good'
        message = "All farms are doing well"
    
    return {
        'status': status,
        'message': message,
        'distribution': health_counts,
        'total_records': total_records
    }

def get_health_score(health_status):
    """Convert health status to numeric score for analytics"""
    scores = {
        'critical': 1,
        'poor': 2,
        'fair': 3,
        'good': 4,
        'excellent': 5
    }
    return scores.get(health_status, 3)

def get_weather_data(latitude, longitude):
    """
    Get weather data for given coordinates
    Replace with actual weather API implementation
    """
    # This is a mock implementation
    # In production, integrate with OpenWeatherMap, WeatherAPI, or similar service
    
    try:
        # Mock weather data
        import random
        
        mock_data = {
            'current': {
                'temperature': round(25 + random.uniform(-5, 10), 1),
                'humidity': round(60 + random.uniform(-20, 30)),
                'wind_speed': round(random.uniform(0, 10), 1),
                'pressure': round(1010 + random.uniform(-20, 20)),
                'visibility': round(8 + random.uniform(-3, 7), 1),
                'description': random.choice(['Clear sky', 'Partly cloudy', 'Cloudy', 'Light rain']),
                'uv_index': round(random.uniform(1, 11), 1),
                'last_updated': timezone.now().isoformat()
            },
            'forecast': []
        }
        
        # Generate 7-day forecast
        for i in range(1, 8):
            date = timezone.now().date() + timedelta(days=i)
            mock_data['forecast'].append({
                'date': date.isoformat(),
                'high_temp': round(23 + random.uniform(-3, 12)),
                'low_temp': round(15 + random.uniform(-3, 8)),
                'humidity': round(60 + random.uniform(-20, 30)),
                'description': random.choice(['Sunny', 'Partly cloudy', 'Cloudy', 'Rain showers']),
                'precipitation_chance': round(random.uniform(0, 100))
            })
        
        return mock_data
        
    except Exception as e:
        return {
            'error': f'Weather data unavailable: {str(e)}',
            'current': None,
            'forecast': []
        }

def get_crop_recommendations(farm):
    """Get AI-powered crop recommendations based on farm data"""
    # This would integrate with agricultural APIs or AI services
    # For now, return mock recommendations
    
    recommendations = {
        'watering': 'Monitor soil moisture levels. Consider irrigation if no rain in next 3 days.',
        'fertilization': 'Apply nitrogen-rich fertilizer in 2 weeks for optimal growth.',
        'pest_control': 'Regular inspection recommended. Watch for early signs of pest activity.',
        'harvest_timing': 'Harvest window appears optimal in 2-3 weeks based on current growth rate.'
    }
    
    return recommendations