from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone_number', 'location', 'is_farmer', 'date_joined')
    list_filter = ('is_farmer', 'is_staff', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'phone_number', 'location')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': ('phone_number', 'location', 'is_farmer')
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {
            'fields': ('email', 'phone_number', 'location', 'is_farmer')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
