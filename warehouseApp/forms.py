from django import forms
from .models import Warehouse, WarehouseCost


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name', 'region', 'capacity', 'field_agent', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'field_agent': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class WarehouseCostForm(forms.ModelForm):
    class Meta:
        model = WarehouseCost
        fields = [
            'warehouse',
            'field_agent',
            'month',
            'rent_cost',
            'handling_cost',
            'electricity_cost',
            'wastage_loss',
            'misc_cost'
        ]

        widgets = {
            'warehouse': forms.Select(attrs={'class': 'form-control'}),
            'field_agent': forms.Select(attrs={'class': 'form-control'}),
            'month': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'rent_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'handling_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'electricity_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'wastage_loss': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'misc_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
        }
