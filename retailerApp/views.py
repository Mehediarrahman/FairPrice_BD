from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import RetailerProfile, Product, RetailerProductPrice
from .forms import RetailerProfileForm, ProductForm, RetailerProductPriceForm
from accountsApp.models import Region
from farmarApp.models import Crop, FieldAgent

@login_required
def retailer_dashboard(request):
    # Check if retailer profile exists, if not create one
    try:
        retailer_profile = request.user.retailerprofile
    except RetailerProfile.DoesNotExist:
        retailer_profile = None
    
    # Get retailer's product prices
    if retailer_profile:
        product_prices = RetailerProductPrice.objects.filter(retailer=retailer_profile)
    else:
        product_prices = []
    
    context = {
        'retailer_profile': retailer_profile,
        'product_prices': product_prices,
    }
    return render(request, 'retailerApp/dashboard.html', context)

@login_required
def create_retailer_profile(request):
    try:
        # Check if profile already exists
        retailer_profile = request.user.retailerprofile
        messages.info(request, 'You already have a retailer profile.')
        return redirect('retailer_dashboard')
    except RetailerProfile.DoesNotExist:
        pass

    if request.method == 'POST':
        form = RetailerProfileForm(request.POST)
        if form.is_valid():
            retailer_profile = form.save(commit=False)
            retailer_profile.user = request.user
            retailer_profile.save()
            messages.success(request, 'Retailer profile created successfully!')
            return redirect('retailer_dashboard')
    else:
        form = RetailerProfileForm()
    
    context = {
        'form': form,
        'title': 'Create Retailer Profile'
    }
    return render(request, 'retailerApp/retailer_profile_form.html', context)

@login_required
def update_retailer_profile(request):
    try:
        retailer_profile = request.user.retailerprofile
    except RetailerProfile.DoesNotExist:
        messages.error(request, 'Please create a retailer profile first.')
        return redirect('create_retailer_profile')

    if request.method == 'POST':
        form = RetailerProfileForm(request.POST, instance=retailer_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Retailer profile updated successfully!')
            return redirect('retailer_dashboard')
    else:
        form = RetailerProfileForm(instance=retailer_profile)
    
    context = {
        'form': form,
        'title': 'Update Retailer Profile'
    }
    return render(request, 'retailerApp/retailer_profile_form.html', context)

@login_required
def product_list(request):
    products = Product.objects.all().select_related('crop')
    context = {
        'products': products
    }
    return render(request, 'retailerApp/product_list.html', context)

@login_required
def create_product_price(request):
    try:
        retailer_profile = request.user.retailerprofile
    except RetailerProfile.DoesNotExist:
        messages.error(request, 'Please create a retailer profile first.')
        return redirect('create_retailer_profile')

    if request.method == 'POST':
        form = RetailerProductPriceForm(request.POST)
        if form.is_valid():
            product_price = form.save(commit=False)
            product_price.retailer = retailer_profile
            product_price.save()
            messages.success(request, 'Product price added successfully!')
            return redirect('retailer_dashboard')
    else:
        form = RetailerProductPriceForm()
    
    context = {
        'form': form,
        'title': 'Add Product Price'
    }
    return render(request, 'retailerApp/product_price_form.html', context)

@login_required
def update_product_price(request, pk):
    try:
        retailer_profile = request.user.retailerprofile
    except RetailerProfile.DoesNotExist:
        messages.error(request, 'Please create a retailer profile first.')
        return redirect('create_retailer_profile')

    product_price = get_object_or_404(RetailerProductPrice, pk=pk, retailer=retailer_profile)

    if request.method == 'POST':
        form = RetailerProductPriceForm(request.POST, instance=product_price)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product price updated successfully!')
            return redirect('retailer_dashboard')
    else:
        form = RetailerProductPriceForm(instance=product_price)
    
    context = {
        'form': form,
        'title': 'Update Product Price'
    }
    return render(request, 'retailerApp/product_price_form.html', context)

@login_required
def delete_product_price(request, pk):
    try:
        retailer_profile = request.user.retailerprofile
    except RetailerProfile.DoesNotExist:
        messages.error(request, 'Please create a retailer profile first.')
        return redirect('create_retailer_profile')

    product_price = get_object_or_404(RetailerProductPrice, pk=pk, retailer=retailer_profile)
    
    if request.method == 'POST':
        product_price.delete()
        messages.success(request, 'Product price deleted successfully!')
        return redirect('retailer_dashboard')
    
    context = {
        'product_price': product_price
    }
    return render(request, 'retailerApp/delete_product_price.html', context)

# AJAX view to load products based on crop selection
def load_products(request):
    crop_id = request.GET.get('crop_id')
    products = Product.objects.filter(crop_id=crop_id).order_by('name')
    return JsonResponse(list(products.values('id', 'name')), safe=False)