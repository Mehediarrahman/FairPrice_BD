from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('FARMER', 'Farmer'),
        ('WAREHOUSE', 'Warehouse'),
        ('RETAILER', 'Retailer'),
        ('MONITORING_AGENT', 'Monitoring Agent'),
        ('ADMIN', 'Admin'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(null=True)
    
    def str(self):
        return f"{self.username} - {self.role}"
# Create your models here(model done).
#upload
#do Again
