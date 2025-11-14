from django.contrib import admin
from .models import MarketScan, PriceSnapshot, APIToken

admin.site.register(MarketScan)
admin.site.register(PriceSnapshot)
admin.site.register(APIToken)
