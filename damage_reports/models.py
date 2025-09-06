from django.db import models
from django.contrib.auth import get_user_model
from farms.models import Farm

User = get_user_model()

class DamageReport(models.Model):
    DAMAGE_TYPES = [
        ('flood', 'Flood Damage'),
        ('drought', 'Drought Damage'),
        ('storm', 'Storm Damage'),
        ('pest', 'Pest Infestation'),
        ('disease', 'Plant Disease'),
        ('frost', 'Frost Damage'),
        ('hail', 'Hail Damage'),
        ('other', 'Other'),
    ]
    
    SEVERITY_LEVELS = [
        ('minor', 'Minor (0-25% damage)'),
        ('moderate', 'Moderate (26-50% damage)'),
        ('major', 'Major (51-75% damage)'),
        ('severe', 'Severe (76-100% damage)'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
    ]
    
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='damage_reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    damage_type = models.CharField(max_length=20, choices=DAMAGE_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    title = models.CharField(max_length=200)
    description = models.TextField()
    estimated_loss_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    estimated_financial_loss = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    date_occurred = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.farm.name} - {self.damage_type} - {self.date_occurred}"

class DamagePhoto(models.Model):
    damage_report = models.ForeignKey(DamageReport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='damage_photos/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Photo for {self.damage_report.title}"
