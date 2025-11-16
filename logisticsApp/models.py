from django.db import models
from django.contrib.auth.models import User
from accountsApp.models import UserProfile
from farmarApp.models import Crop


# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Transporter(models.Model):
    VEHICLE_TYPES = [
        ('TRUCK', 'Truck'),
        ('VAN', 'Van'),
        ('PICKUP', 'Pickup'),
        ('TRAILER', 'Trailer'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
    ]
    
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.vehicle_type}"

class TransportTrip(models.Model):
    transporter = models.ForeignKey(Transporter, on_delete=models.CASCADE, related_name='trips')
    origin_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='origin_trips')
    destination_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='destination_trips')
    field_agent = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'userprofile__role': 'MONITORING_AGENT'})
    product = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity in kg")
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Transport cost in BDT")
    trip_date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Trip #{self.id} - {self.origin_region} to {self.destination_region}"
    
    def cost_per_kg(self):
        if self.quantity > 0:
            return self.cost / self.quantity
        return 0