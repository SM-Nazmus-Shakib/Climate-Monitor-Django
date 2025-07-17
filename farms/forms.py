from django import forms
from .models import Farm, Crop

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['name', 'address', 'latitude', 'longitude', 'size', 'soil_type']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
    def save(self, commit=True):
        farm = super().save(commit=False)
        if self.user:
            farm.owner = self.user
        if commit:
            farm.save()
        return farm

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['crop_type', 'variety', 'planting_date', 'expected_harvest_date', 'current_status', 'notes']
        widgets = {
            'planting_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_harvest_date': forms.DateInput(attrs={'type': 'date'}),
        }