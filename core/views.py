from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'core/home.html')  

def no_permission(request):
    return render(request, 'core/no_permission.html')

@login_required
def climate_dashboard(request):
    return render(request, 'core/climate_dashboard.html')