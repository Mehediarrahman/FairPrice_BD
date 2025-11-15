from django.db import models
from django.contrib.auth.models import User


class Region(models.Model):
    REGION_TYPES = (
        ('division', 'Division'),
        ('district', 'District'),
        ('upazila', 'Upazila'),
    )

    name = models.CharField(max_length=200)
    parent_region = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)
    region_type = models.CharField(max_length=20, choices=REGION_TYPES)

    def __str__(self):
        return self.name


class FieldAgent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    phone = models.CharField(max_length=20,null=True)
    status = models.CharField(max_length=20, null=True, default="Active")
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()


class Farmer(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    nid_number = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    field_agent_assignment = models.ForeignKey('FieldAgentAssignment', null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class FieldAgentAssignment(models.Model):
    field_agent = models.ForeignKey(FieldAgent, on_delete=models.CASCADE)
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, default="active")

    def __str__(self):
        return f"{self.field_agent} → {self.farmer}"


class Crop(models.Model):
    name = models.CharField(max_length=200,null=True)
    season = models.CharField(max_length=100,null=True)
    unit = models.CharField(max_length=50,null=True)

    def __str__(self):
        return self.name


class FarmRecord(models.Model):
    STATUS = (
        ('growing', 'Growing'),
        ('harvested', 'Harvested'),
        ('completed', 'Completed'),
    )
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    field_agent = models.ForeignKey(FieldAgent, null=True, on_delete=models.SET_NULL)
    region = models.ForeignKey(Region, null=True, on_delete=models.SET_NULL)
    land_area = models.FloatField(null=True)
    expected_yield = models.FloatField(null=True)
    harvest_date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=STATUS, default="growing")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farmer} - {self.crop}"


class CropExpense(models.Model):
    CATEGORY = (
        ('seed', 'Seed'),
        ('fertilizer', 'Fertilizer'),
        ('labor', 'Labor'),
        ('pesticide', 'Pesticide'),
        ('irrigation', 'Irrigation'),
        ('other', 'Other'),
    )

    farm_record = models.ForeignKey(FarmRecord, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=CATEGORY,null=True)
    amount = models.FloatField(null=True)
    note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.farm_record} - {self.category}"
