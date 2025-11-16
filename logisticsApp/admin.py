from django.contrib import admin
from logisticsApp.models import *

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'created_at']
    search_fields = ['name', 'code']

@admin.register(Transporter)
class TransporterAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'vehicle_type', 'license_number', 'status', 'created_at']
    list_filter = ['vehicle_type', 'status', 'created_at']
    search_fields = ['name', 'phone', 'license_number']

@admin.register(TransportTrip)
class TransportTripAdmin(admin.ModelAdmin):
    list_display = ['id', 'transporter', 'origin_region', 'destination_region', 'product', 'quantity', 'cost', 'trip_date']
    list_filter = ['trip_date', 'origin_region', 'destination_region', 'product']
    search_fields = ['transporter__name', 'product__name']