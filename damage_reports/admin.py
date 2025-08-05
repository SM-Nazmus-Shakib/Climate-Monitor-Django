from django.contrib import admin
from .models import DamageReport, DamagePhoto

class DamagePhotoInline(admin.TabularInline):
    model = DamagePhoto
    extra = 1

@admin.register(DamageReport)
class DamageReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'farm', 'reporter', 'damage_type', 'severity', 'status', 'date_occurred')
    list_filter = ('damage_type', 'severity', 'status', 'date_occurred', 'created_at')
    search_fields = ('title', 'farm__name', 'reporter__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [DamagePhotoInline]
    
    fieldsets = (
        ('Report Information', {
            'fields': ('farm', 'reporter', 'title', 'description')
        }),
        ('Damage Details', {
            'fields': ('damage_type', 'severity', 'date_occurred')
        }),
        ('Financial Impact', {
            'fields': ('estimated_loss_percentage', 'estimated_financial_loss')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DamagePhoto)
class DamagePhotoAdmin(admin.ModelAdmin):
    list_display = ('damage_report', 'caption', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('damage_report__title', 'caption')