from django.db import models
from accountsApp.models import User
from retailerApp.models import *
from farmarApp.models import *

class MarketScan(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    field_agent = models.ForeignKey(FieldAgent, on_delete=models.CASCADE, null=True)
    photo = models.ImageField(upload_to='market_photos/', null=True)
    observed_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.product.name
    
class PriceSnapshot(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,null=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.product.name}-{self.region.name}'

class APIToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
