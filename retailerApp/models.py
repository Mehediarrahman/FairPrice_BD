from django.db import models
from accountsApp.models import User

class RetailerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    shop_name = models.CharField(max_length=100,null=True)
    trade_license = models.CharField(max_length=50,null=True)
    location = models.CharField(max_length=100,null=True)
    
    def str(self):
        return f"{self.shop_name} - {self.user.username}"

class RetailerStock(models.Model):
    retailer = models.ForeignKey(RetailerProfile, on_delete=models.CASCADE,null=True)
    stock_out = models.ForeignKey('warehouseapp.StockOut', on_delete=models.CASCADE,null=True)
    selling_price_per_kg = models.DecimalField(max_digits=8, decimal_places=2,null=True)
    is_approved = models.BooleanField(default=False,null=True)
    
    def str(self):
        return f"RetailerStock - {self.retailer.shop_name}"