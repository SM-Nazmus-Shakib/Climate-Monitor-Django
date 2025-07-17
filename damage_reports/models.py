from django.db import models
from django.contrib.auth import get_user_model
from farms.models import Farm

User = get_user_model()

DAMAGE_TYPES = [
    ('flood', 'Flood'),
    ('drought', 'Drought'),
    ('storm', 'Storm'),
    ('pest', 'Pest Attack'),
    ('disease', 'Crop Disease'),
    ('other', 'Other'),
]

SEVERITY_CHOICES = [
    (1, 'Low'),
    (2, 'Medium'),
    (3, 'High'),
]

class DamageReport(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='damage_reports')
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    damage_type = models.CharField(max_length=50, choices=DAMAGE_TYPES)
    description = models.TextField()
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    date_reported = models.DateTimeField(auto_now_add=True)
    date_occurred = models.DateField()
    estimated_loss = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_reports')
    verification_notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date_reported']
        permissions = [
            ('can_verify_reports', 'Can verify damage reports'),
        ]
        
    def __str__(self):
        return f"{self.get_damage_type_display()} at {self.farm.name} ({self.date_occurred})"