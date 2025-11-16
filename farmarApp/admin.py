from django.contrib import admin
from .models import *
admin.site.register([Region,FieldAgent,Farmer,FieldAgentAssignment,Crop,FarmRecord,CropExpense])
# Register your models here.
