from django.db import models
from warehouseApp.models import*
from retailerApp.models import *

class Transport(models.Model):
    company_name = models.CharField(max_length=100,null=True)
    vehicle_number = models.CharField(max_length=20,null=True)
    driver_details = models.TextField(null=True)
    
    def str(self):
        return f"{self.company_name} - {self.vehicle_number}"

class DeliveryChalan(models.Model):
    STATUS_CHOICES = (
        ('dispatched', 'Dispatched'),
        ('in_transit', 'In Transit'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    transport = models.ForeignKey(Transport, on_delete=models.CASCADE,null=True)
    stock_out = models.OneToOneField(StockOut, on_delete=models.CASCADE,null=True)
    source_warehouse = models.ForeignKey('warehouseapp.WarehouseProfile', on_delete=models.CASCADE,null=True)
    destination_retailer = models.ForeignKey(RetailerProfile, on_delete=models.CASCADE,null=True)
    dispatch_time = models.DateTimeField(null=True)
    received_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='dispatched',null=True)
    
    def str(self):
        return f"DeliveryChalan - {self.stock_out.id}"