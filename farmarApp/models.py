from django.db import models
from accountsApp.models import *

class Crop(models.Model):
    name = models.CharField(max_length=100,null=True)  
    season = models.CharField(max_length=50,null=True)
    
    def str(self):
        return f"{self.name} - {self.season}"
    

class FieldAgent(models.Model):
    Status=[
        ('Active','Active'),    
        ('Inactive','Inactive'),    
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=150,null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,null=True,null=True)
    phone = models.CharField(max_length=50,null=True)
    status = models.CharField(choices=Status, max_length=50,null=True)
    joined_date = models.DateField(auto_now_add=True,null=True)

    def str(self):
        return f"{self.name} - {self.status}"





class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    name = models.CharField(max_length=20,null=True)
    nid_number = models.IntegerField(null=True)
    phone = models.CharField(max_length=50,null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,null=True,null=True)
    field_agent_assignment = models.ForeignKey(FieldAgent , on_delete=models.CASCADE,null=True,null=True)
    created_at = models.DateField(auto_now_add=True,null=True)
    
    
    def str(self):
        return f"{self.user.username} - {self.region}"

class FarmRecord(models.Model):
    Status=[
        ('Growing','Growing'),    
        ('Harvested','Harvested'),    
        ('etc','etc'),    
    ]
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE,null=True)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE,null=True)
    field_agent_assignment = models.ForeignKey(FieldAgent , on_delete=models.CASCADE,null=True,null=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE,null=True,null=True)
    land_area = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    expected_yield = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    harvest_date = models.DateField(auto_now_add=True,null=True)
    status = models.CharField(choices=Status, max_length=50,null=True)
    created_at = models.DateField(auto_now_add=True,null=True)
    
    
    def str(self):
        return f"{self.farmer.user.username} - {self.crop.name}"
    

class CropExpense(models.Model):
    Expense=[
        ('Seed','Seed'),
        ('Fertilizer','Fertilizer'),
        ('Labor','Labor'),
        ('Pesticide','Pesticide'),
        ('iIrrigation','iIrrigation'),
        ('etc','etc'),

    ]
    farm_record = models.ForeignKey(FarmRecord, on_delete=models.CASCADE,null=True)
    category = models.CharField(choices=Expense, max_length=50,null=True)
    amount = models.DecimalField(max_digits=5, decimal_places=2,null=True)
    note = models.CharField(max_length=250,null=True)
    created_at = models.DateField(auto_now_add=True,null=True)

    def str(self):
        return f"{self.farm_record.farmer.user.username} - {self.season}"

class FieldAgentAssignment(models.Model):
    Status=[
        ('Active','Active'),    
        ('Completed','Completed'),   
    ]
    field_agent = models.ForeignKey(FieldAgent, on_delete=models.CASCADE,null=True)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE,null=True)
    assigned_date = models.DateField(auto_now_add=True,null=True)
    status = models.CharField(choices=Status, max_length=50,null=True)

    def str(self):
        return f"{self.field_agent.name} - {self.status}"