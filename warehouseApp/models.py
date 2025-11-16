from django.db import models
from accountsApp.models import User
from farmarApp.models import *


class Warehouse(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    name = models.CharField(max_length=200)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='warehouses')
    capacity = models.FloatField(help_text="Capacity in tons")
    field_agent = models.ForeignKey(FieldAgent, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WarehouseCost(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='costs')
    field_agent = models.ForeignKey(FieldAgent, on_delete=models.SET_NULL, null=True, blank=True)
    month = models.DateField(help_text="Use any date inside the month")

    rent_cost = models.FloatField(default=0)
    handling_cost = models.FloatField(default=0)
    electricity_cost = models.FloatField(default=0)
    wastage_loss = models.FloatField(default=0)
    misc_cost = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-month']
        unique_together = ('warehouse', 'month')  # Prevent double-entry for same month

    def __str__(self):
        return f"{self.warehouse.name} - {self.month.strftime('%B %Y')}"

    @property
    def total_cost(self):
        return (
            self.rent_cost +
            self.handling_cost +
            self.electricity_cost +
            self.wastage_loss +
            self.misc_cost
        )
