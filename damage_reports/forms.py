from django import forms
from .models import DamageReport
from farms.models import Farm
from django.contrib.auth import get_user_model

User = get_user_model()

class DamageReportForm(forms.ModelForm):
    class Meta:
        model = DamageReport
        fields = ['farm', 'damage_type', 'description', 'severity', 'date_occurred', 'estimated_loss']
        widgets = {
            'date_occurred': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['farm'].queryset = Farm.objects.filter(owner=user)

class DamageReportVerificationForm(forms.ModelForm):
    class Meta:
        model = DamageReport
        fields = ['verification_notes', 'is_verified']
        widgets = {
            'verification_notes': forms.Textarea(attrs={'rows': 4}),
        }