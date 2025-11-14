from django import forms
from .models import MarketScan,PriceSnapshot

class MarketScanForm(forms.ModelForm):
    class Meta:
        model = MarketScan
        fields = ["product", "region", "photo", "observed_price", "remarks"]

class PriceSnapshotForm(forms.ModelForm):
    class Meta:
        model = PriceSnapshot
        fields = ["product", "region", "average_price"]
