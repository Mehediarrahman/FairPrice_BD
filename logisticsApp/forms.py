from django import forms
from logisticsApp.models import *
from django.contrib.auth.models import User

class TransporterForm(forms.ModelForm):
    class Meta:
        model = Transporter
        fields = ['name', 'phone', 'vehicle_type', 'license_number', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter transporter name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'vehicle_type': forms.Select(attrs={'class': 'form-control'}),
            'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter license number'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class TransportTripForm(forms.ModelForm):
    class Meta:
        model = TransportTrip
        fields = ['transporter', 'origin_region', 'destination_region', 'field_agent', 'product', 'quantity', 'cost', 'trip_date', 'notes']
        widgets = {
            'transporter': forms.Select(attrs={'class': 'form-control'}),
            'origin_region': forms.Select(attrs={'class': 'form-control'}),
            'destination_region': forms.Select(attrs={'class': 'form-control'}),
            'field_agent': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity in kg', 'step': '0.01'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cost in BDT', 'step': '0.01'}),
            'trip_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show monitoring agents in field_agent dropdown
        self.fields['field_agent'].queryset = User.objects.filter(userprofile__role='MONITORING_AGENT')