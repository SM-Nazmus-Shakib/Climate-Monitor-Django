from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Farm, Crop
from .forms import FarmForm, CropForm
from weather.views import fetch_weather_data

@login_required
def farm_map(request):
    farms = Farm.objects.filter(owner=request.user)
    
    # Prepare map data
    map_data = {
        'farms': [],
        'default_lat': 23.6850,  # Default to Bangladesh coordinates
        'default_lng': 90.3563,
        'default_zoom': 7
    }
    
    for farm in farms:
        weather_data = fetch_weather_data(farm.latitude, farm.longitude) or {}
        
        map_data['farms'].append({
            'id': farm.id,
            'name': farm.name,
            'lat': farm.latitude,
            'lng': farm.longitude,
            'weather_icon': weather_data.get('icon', 'wi wi-day-sunny'),
            'temperature': weather_data.get('temperature', 'N/A'),
            'conditions': weather_data.get('conditions', 'Clear')
        })
    
    return render(request, 'farms/map.html', map_data)

@login_required
def farm_list(request):
    farms = Farm.objects.filter(owner=request.user)
    return render(request, 'farms/list.html', {'farms': farms})

@login_required
def farm_detail(request, pk):
    farm = get_object_or_404(Farm, pk=pk, owner=request.user)
    crops = farm.crops.all()
    weather_data = farm.weather_data.filter(is_forecast=False).order_by('-recorded_at')[:10]
    
    return render(request, 'farms/farm_detail.html', {
        'farm': farm,
        'crops': crops,
        'weather_data': weather_data
    })

@login_required
def add_farm(request):
    if request.method == 'POST':
        form = FarmForm(request.POST, user=request.user)
        if form.is_valid():
            farm = form.save()
            messages.success(request, 'Farm added successfully!')
            return redirect('farms:detail', pk=farm.pk)
    else:
        form = FarmForm(user=request.user)
    
    return render(request, 'farms/add_farm.html', {'form': form})

@login_required
def add_crop(request, farm_id):
    farm = get_object_or_404(Farm, pk=farm_id, owner=request.user)
    
    if request.method == 'POST':
        form = CropForm(request.POST)
        if form.is_valid():
            crop = form.save(commit=False)
            crop.farm = farm
            crop.save()
            messages.success(request, 'Crop added successfully!')
            return redirect('farms:detail', pk=farm.pk)
    else:
        form = CropForm()
    
    return render(request, 'farms/add_crop.html', {'form': form, 'farm': farm})