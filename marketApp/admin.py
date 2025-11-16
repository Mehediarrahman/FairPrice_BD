from django.contrib import admin
from .models import MarketScan, PriceSnapshot

admin.site.register(MarketScan)
admin.site.register(PriceSnapshot)
