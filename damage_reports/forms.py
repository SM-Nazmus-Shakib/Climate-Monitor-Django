from django import forms
from .models import DamageReport, DamagePhoto

class DamageReportForm(forms.ModelForm):
    class Meta:
        model = DamageReport
        fields = ['farm', 'damage_type', 'severity', 'title', 'description', 
                 'estimated_loss_percentage', 'estimated_financial_loss', 'date_occurred']
        widgets = {
            'date_occurred': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }
    
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm'].queryset = user.farms.all()

class DamagePhotoForm(forms.ModelForm):
    class Meta:
        model = DamagePhoto
        fields = ['image', 'caption']