from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Farm, CropMonitoring
from .forms import FarmForm, CropMonitoringForm

@login_required
def dashboard(request):
    farms = Farm.objects.filter(owner=request.user)
    context = {
        'farms': farms,
        'total_farms': farms.count(),
        'total_area': sum(farm.area_acres for farm in farms),
    }
    return render(request, 'farms/dashboard.html', context)

@login_required
def farm_list(request):
    farms = Farm.objects.filter(owner=request.user)
    return render(request, 'farms/farm_list.html', {'farms': farms})

@login_required
def farm_detail(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, owner=request.user)
    monitoring_records = CropMonitoring.objects.filter(farm=farm).order_by('-recorded_at')
    
    if request.method == 'POST':
        form = CropMonitoringForm(request.POST)
        if form.is_valid():
            monitoring = form.save(commit=False)
            monitoring.farm = farm
            monitoring.save()
            messages.success(request, 'Crop monitoring record added successfully!')
            return redirect('farms:farm_detail', farm_id=farm.id)
    else:
        form = CropMonitoringForm()
    
    context = {
        'farm': farm,
        'monitoring_records': monitoring_records,
        'form': form,
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
            messages.success(request, 'Farm added successfully!')
            return redirect('farms:farm_list')
    else:
        form = FarmForm()
    return render(request, 'farms/farm_form.html', {'form': form, 'title': 'Add New Farm'})

@login_required
def farm_edit(request, farm_id):
    farm = get_object_or_404(Farm, id=farm_id, owner=request.user)
    if request.method == 'POST':
        form = FarmForm(request.POST, instance=farm)
        if form.is_valid():
            form.save()
            messages.success(request, 'Farm updated successfully!')
            return redirect('farms:farm_detail', farm_id=farm.id)
    else:
        form = FarmForm(instance=farm)
    return render(request, 'farms/farm_form.html', {'form': form, 'title': 'Edit Farm', 'farm': farm})
