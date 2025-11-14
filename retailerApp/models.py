from django.db import models
from accountsApp.models import *
from farmarApp.models import *

class RetailerProfile(models.Model):
    Status=[
        ('Active','Active'),    
        ('In Active','In Active'),    
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    shop_name = models.CharField(max_length=100,null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,null=True)
    field_agent = models.ForeignKey(FieldAgent, on_delete=models.CASCADE,null=True)
    phone  = models.CharField(max_length=150, null=True)
    status = models.CharField(choices=Status, max_length=50, null=True)
    
    def str(self):
        return f"{self.shop_name} - {self.user.username}"
    
class Product(models.Model):
    Unit=[
        ('Kg','Kg'),    
        ('Liter','Liter'),    
        ('etc','etc'),    
    ]
    Category=[
        ('Food','Food'),    
        ('Vegetable','Vegetable'),    
        ('etc','etc'),    
    ]
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE,null=True)
    name = models.CharField( max_length=250, null=True)
    unit = models.CharField(choices=Unit, max_length=50,null=True)
    catagory = models.CharField(choices=Category, max_length=50,null=True)
    created_at = models.DateField(auto_now_add=True,null=True)


class RetailerProductPrice(models.Model):
    retailer = models.ForeignKey(RetailerProfile, on_delete=models.CASCADE,null=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE,null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,null=True)
    field_agent = models.ForeignKey(FieldAgent, on_delete=models.CASCADE,null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    created_at = models.DateField(auto_now_add=True,null=True)
    verified = models.BooleanField(default=False,null=True)
    
    def str(self):
        return f"Retailer: - {self.retailer.shop_name}"