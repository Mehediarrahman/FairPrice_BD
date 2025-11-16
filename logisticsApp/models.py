from django.db import models
from warehouseApp.models import*
from retailerApp.models import *

class Transport(models.Model):
    company_name = models.CharField(max_length=100,null=True)
    vehicle_number = models.CharField(max_length=20,null=True)
    driver_details = models.TextField(null=True)
    
    def str(self):
        return f"{self.company_name} - {self.vehicle_number}"

# Create your models here.

class Region(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE,null=True)
    stock_out = models.OneToOneField(StockOut, on_delete=models.CASCADE,null=True)
    source_warehouse = models.ForeignKey('warehouseapp.WarehouseProfile', on_delete=models.CASCADE,null=True)
    destination_retailer = models.ForeignKey(RetailerProfile, on_delete=models.CASCADE,null=True)
    dispatch_time = models.DateTimeField(null=True)
    received_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dispatched',null=True)
    
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