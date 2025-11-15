from django import forms
from .models import RetailerProfile, Product, RetailerProductPrice
from accountsApp.models import User, Region
from farmarApp.models import FieldAgent, Crop

class RetailerProfileForm(forms.ModelForm):
    class Meta:
        model = RetailerProfile
        fields = ['shop_name', 'region', 'field_agent', 'phone', 'status']
        widgets = {
            'shop_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter shop name'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'field_agent': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['crop', 'name', 'unit', 'catagory']
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'unit': forms.Select(attrs={'class': 'form-control'}),
            'catagory': forms.Select(attrs={'class': 'form-control'}),
        }

class RetailerProductPriceForm(forms.ModelForm):
    class Meta:
        model = RetailerProductPrice
        fields = ['crop', 'product', 'region', 'field_agent', 'price']
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'product': forms.Select(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'field_agent': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price', 'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.none()

        if 'crop' in self.data:
            try:
                crop_id = int(self.data.get('crop'))
                self.fields['product'].queryset = Product.objects.filter(crop_id=crop_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['product'].queryset = self.instance.crop.product_set.order_by('name')