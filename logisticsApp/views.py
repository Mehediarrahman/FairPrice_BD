from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg, Count, Sum
from logisticsApp.models import *
from logisticsApp.forms import *

@login_required
def logistics_dashboard(request):
    # Check if user has permission to access logistics
    if request.user.userprofile.role not in ['MONITORING_AGENT', 'ADMIN']:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('accounts:login')
    
    # Get statistics
    total_transporters = Transporter.objects.count()
    active_transporters = Transporter.objects.filter(status='ACTIVE').count()
    total_trips = TransportTrip.objects.count()
    
    # Get average transport cost per kg
    avg_cost_data = TransportTrip.objects.aggregate(
        avg_cost_per_kg=Avg('cost') / Avg('quantity')
    )
    
    context = {
        'total_transporters': total_transporters,
        'active_transporters': active_transporters,
        'total_trips': total_trips,
        'avg_cost_per_kg': avg_cost_data['avg_cost_per_kg'] or 0,
    }
    return render(request, 'logicticsApp/logistics_dashboard.html', context)

@login_required
def transporter_list(request):
    if request.user.userprofile.role not in ['MONITORING_AGENT', 'ADMIN']:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    transporters = Transporter.objects.all().order_by('-created_at')
    return render(request, 'logicticsApp/transporter_list.html', {'transporters': transporters})

@login_required
def add_transporter(request):
    if request.user.userprofile.role not in ['MONITORING_AGENT', 'ADMIN']:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = TransporterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transporter added successfully!')
            return redirect('logicticsApp:transporter_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TransporterForm()
    
    return render(request, 'logicticsApp/transporter_form.html', {'form': form, 'title': 'Add Transporter'})

@login_required
def edit_transporter(request, pk):
    if request.user.userprofile.role not in ['MONITORING_AGENT', 'ADMIN']:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    try:
        transporter = Transporter.objects.get(pk=pk)
    except Transporter.DoesNotExist:
        messages.error(request, 'Transporter not found.')
        return redirect('logicticsApp:transporter_list')
    
    if request.method == 'POST':
        form = TransporterForm(request.POST, instance=transporter)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transporter updated successfully!')
            return redirect('logicticsApp:transporter_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TransporterForm(instance=transporter)
    
    return render(request, 'logicticsApp/transporter_form.html', {'form': form, 'title': 'Edit Transporter'})

@login_required
def trip_list(request):
    if request.user.userprofile.role not in ['MONITORING_AGENT', 'ADMIN']:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    trips = TransportTrip.objects.all().order_by('-trip_date', '-created_at')
    return render(request, 'logicticsApp/trip_list.html', {'trips': trips})

@login_required
def add_trip(request):
    if request.user.userprofile.role not in ['MONITORING_AGENT', 'ADMIN']:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    if request.method == 'POST':
        form = TransportTripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
            # If the user is a monitoring agent, auto-assign them
            if request.user.userprofile.role == 'MONITORING_AGENT':
                trip.field_agent = request.user
            trip.save()
            messages.success(request, 'Transport trip logged successfully!')
            return redirect('logicticsApp:trip_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TransportTripForm()
        # If user is monitoring agent, set them as default field agent
        if request.user.userprofile.role == 'MONITORING_AGENT':
            form.fields['field_agent'].initial = request.user
    
    return render(request, 'logicticsApp/trip_form.html', {'form': form, 'title': 'Log Transport Trip'})

@login_required
def transport_analytics(request):
    if request.user.userprofile.role not in ['MONITORING_AGENT', 'ADMIN']:
        messages.error(request, "Access denied.")
        return redirect('accounts:login')
    
    # Calculate average transport cost per route and product
    route_analytics = TransportTrip.objects.values(
        'origin_region__name', 
        'destination_region__name', 
        'product__name'
    ).annotate(
        total_trips=Count('id'),
        avg_cost_per_kg=Avg('cost') / Avg('quantity'),
        total_quantity=Sum('quantity')
    ).order_by('origin_region__name', 'destination_region__name')
    
    context = {
        'route_analytics': route_analytics,
    }
    return render(request, 'logicticsApp/transport_analytics.html', context)