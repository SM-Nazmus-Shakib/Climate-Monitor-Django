from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files.storage import default_storage

@require_POST
@csrf_exempt  # Only use this if you're having CSRF issues, otherwise implement proper CSRF handling
def update_profile_picture(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile_picture = request.FILES['profile_picture']
        
        # Validate file size (max 5MB)
        if profile_picture.size > 5 * 1024 * 1024:
            return JsonResponse({'success': False, 'error': 'File size too large. Maximum size is 5MB.'})
        
        # Validate file type
        allowed_types = ['image/jpeg', 'image/png', 'image/gif']
        if profile_picture.content_type not in allowed_types:
            return JsonResponse({'success': False, 'error': 'Invalid file type. Only JPEG, PNG and GIF are allowed.'})
        
        # Save the file to the user's profile
        user = request.user
        file_name = f"profile_pictures/user_{user.id}_{profile_picture.name}"
        
        # Delete old profile picture if exists
        if user.profile_picture:
            if default_storage.exists(user.profile_picture.name):
                default_storage.delete(user.profile_picture.name)
        
        # Save new profile picture
        user.profile_picture.save(file_name, profile_picture)
        user.save()
        
        return JsonResponse({'success': True, 'url': user.profile_picture.url})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('farms:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'user': request.user})
