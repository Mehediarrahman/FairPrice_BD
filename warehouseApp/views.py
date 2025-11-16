from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Avg, F, FloatField
from django.db.models.functions import Coalesce

from .models import Warehouse, WarehouseCost
from .forms import WarehouseForm, WarehouseCostForm


@login_required
def warehouse_list(request):
    warehouses = Warehouse.objects.all().order_by('-id')
    return render(request, 'warehouse/warehouse_list.html', {'warehouses': warehouses})

@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Warehouse created.")
            return redirect('warehouse_list')
    else:
        form = WarehouseForm()
    return render(request, 'warehouse/warehouse_form.html', {'form': form})

@login_required
def warehouse_edit(request, id):
    warehouse = get_object_or_404(Warehouse, id=id)
    if request.method == 'POST':
        form = WarehouseForm(request.POST, instance=warehouse)
        if form.is_valid():
            form.save()
            messages.success(request, "Warehouse updated.")
            return redirect('warehouse_list')
    else:
        form = WarehouseForm(instance=warehouse)
    return render(request, 'warehouse/warehouse_form.html', {'form': form})

@login_required
def warehouse_delete(request, id):
    warehouse = get_object_or_404(Warehouse, id=id)
    warehouse.delete()
    messages.success(request, "Warehouse deleted.")
    return redirect('warehouse_list')


@login_required
def warehouse_cost_list(request):
    costs = WarehouseCost.objects.all().order_by('-month')
    return render(request, 'warehouse/warehouse_cost_list.html', {'costs': costs})

@login_required
def warehouse_cost_create(request):
    if request.method == 'POST':
        form = WarehouseCostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cost added.")
            return redirect('warehouse_cost_list')
    else:
        form = WarehouseCostForm()
    return render(request, 'warehouse/warehouse_cost_form.html', {'form': form})

@login_required
def warehouse_cost_edit(request, id):
    cost = get_object_or_404(WarehouseCost, id=id)
    if request.method == 'POST':
        form = WarehouseCostForm(request.POST, instance=cost)
        if form.is_valid():
            form.save()
            messages.success(request, "Cost updated.")
            return redirect('warehouse_cost_list')
    else:
        form = WarehouseCostForm(instance=cost)
    return render(request, 'warehouse/warehouse_cost_form.html', {'form': form})

@login_required
def warehouse_cost_delete(request, id):
    cost = get_object_or_404(WarehouseCost, id=id)
    cost.delete()
    messages.success(request, "Cost deleted.")
    return redirect('warehouse_cost_list')

@login_required
def region_avg_cost(request):
    """
    Average warehouse cost per region.
    """
    regional_costs = (
        WarehouseCost.objects
        .values('warehouse__region__name')
        .annotate(
            avg_cost=Avg(
                F('rent_cost') +
                F('handling_cost') +
                F('electricity_cost') +
                F('wastage_loss') +
                F('misc_cost')
            )
        )
    )
    return render(request, 'warehouse/region_avg_cost.html', {
        'regional_costs': regional_costs
    })

@login_required
def warehouse_avg_cost(request):
    """
    Average monthly cost per warehouse.
    """
    warehouse_data = []
    for w in Warehouse.objects.all():
        avg_cost = w.costs.aggregate(
            avg=Avg(
                F('rent_cost') +
                F('handling_cost') +
                F('electricity_cost') +
                F('wastage_loss') +
                F('misc_cost')
            )
        )['avg'] or 0
        warehouse_data.append({
            'warehouse': w,
            'avg_cost': avg_cost,
        })
    return render(request, 'warehouse/warehouse_avg_cost.html', {
        'warehouse_data': warehouse_data
    })

@login_required
def avg_warehouse_for_fairprice(request):
    """
    Overall average warehouse cost (for Fair Price formula).
    """
    avg_warehouse = (
        WarehouseCost.objects.aggregate(
            avg_cost=Avg(
                F('rent_cost') +
                F('handling_cost') +
                F('electricity_cost') +
                F('wastage_loss') +
                F('misc_cost')
            )
        )['avg_cost'] or 0
    )
    return render(request, 'warehouse/avg_warehouse.html', {
        'avg_warehouse': avg_warehouse
    })


@login_required
def warehouse_cost_summary(request):
    """
    Show per warehouse total cost, cost per ton, and region-wise average cost.
    """
    warehouses = Warehouse.objects.select_related('region')
    data = []

    for wh in warehouses:
        cost_summary = WarehouseCost.objects.filter(warehouse=wh).aggregate(
            total_rent=Coalesce(Sum('rent_cost'), 0),
            total_handling=Coalesce(Sum('handling_cost'), 0),
            total_electricity=Coalesce(Sum('electricity_cost'), 0),
            total_wastage=Coalesce(Sum('wastage_loss'), 0),
            total_misc=Coalesce(Sum('misc_cost'), 0),
        )

        total_cost = sum(cost_summary.values())
        cost_per_ton = total_cost / wh.capacity if wh.capacity else 0

        data.append({
            'warehouse': wh,
            'region': wh.region.name if wh.region else "",
            'capacity': wh.capacity,
            'total_cost': total_cost,
            'cost_per_ton': round(cost_per_ton, 2),
        })

    region_avg = (
        Warehouse.objects.values('region__name')
        .annotate(
            avg_cost_per_ton=Coalesce(
                Sum(
                    (
                        F('warehousecost__rent_cost') +
                        F('warehousecost__handling_cost') +
                        F('warehousecost__electricity_cost') +
                        F('warehousecost__wastage_loss') +
                        F('warehousecost__misc_cost')
                    ) / F('capacity'),
                    output_field=FloatField()
                ),
                0
            )
        )
    )

    return render(request, 'warehouse/warehouse_cost_summary.html', {
        'data': data,
        'region_avg': region_avg,
    })
