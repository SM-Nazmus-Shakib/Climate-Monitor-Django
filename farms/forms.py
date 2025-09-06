from django import forms
from .models import Farm, CropMonitoring

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'location', 'latitude', 'longitude', 'area_acres', 
                 'crop_type', 'planting_date', 'expected_harvest_date']
        widgets = {
            'planting_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_harvest_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CropMonitoringForm(forms.ModelForm):
    class Meta:
        model = CropMonitoring
        fields = ['health_status', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4}),
        }