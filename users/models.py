from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    is_farmer = models.BooleanField(default=True)
    is_agriculture_officer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.get_full_name() or self.username