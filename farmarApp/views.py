from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import *


def farmer_list(request):
    farmers = Farmer.objects.all()
    return render(request, 'farmer/farmer_list.html', {'farmers': farmers})


def farmer_create(request):
    form = FarmerForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('farmer_list')
    return render(request, 'farmer/farmer_form.html', {'form': form})


def farmer_edit(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    form = FarmerForm(request.POST or None, instance=farmer)
    if form.is_valid():
        form.save()
        return redirect('farmer_list')
    return render(request, 'farmer/farmer_form.html', {'form': form})


def farmer_delete(request, pk):
    farmer = get_object_or_404(Farmer, pk=pk)
    farmer.delete()
    return redirect('farmer_list')


def crop_list(request):
    crops = Crop.objects.all()
    return render(request, 'crop/crop_list.html', {'crops': crops})


def crop_create(request):
    form = CropForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('crop_list')
    return render(request, 'crop/crop_form.html', {'form': form})


def crop_edit(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    form = CropForm(request.POST or None, instance=crop)
    if form.is_valid():
        form.save()
        return redirect('crop_list')
    return render(request, 'crop/crop_form.html', {'form': form})


def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    crop.delete()
    return redirect('crop_list')


def farmrecord_list(request):
    records = FarmRecord.objects.all()
    return render(request, 'farmrecord/farmrecord_list.html', {'records': records})


def farmrecord_create(request):
    form = FarmRecordForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('farmrecord_list')
    return render(request, 'farmrecord/farmrecord_form.html', {'form': form})


def farmrecord_edit(request, pk):
    record = get_object_or_404(FarmRecord, pk=pk)
    form = FarmRecordForm(request.POST or None, instance=record)
    if form.is_valid():
        form.save()
        return redirect('farmrecord_list')
    return render(request, 'farmrecord/farmrecord_form.html', {'form': form})


def farmrecord_delete(request, pk):
    record = get_object_or_404(FarmRecord, pk=pk)
    record.delete()
    return redirect('farmrecord_list')


def farmrecord_detail(request, pk):
    record = get_object_or_404(FarmRecord, pk=pk)
    expenses = CropExpense.objects.filter(farm_record=record)

    total_expense = sum(item.amount for item in expenses)

    if record.expected_yield > 0:
        cost_per_unit = total_expense / record.expected_yield
    else:
        cost_per_unit = 0

    context = {
        'record': record,
        'expenses': expenses,
        'total_expense': total_expense,
        'cost_per_unit': round(cost_per_unit, 2),
    }
    return render(request, 'farmrecord/farmrecord_detail.html', context)


def expense_create(request, farm_id):
    farm = get_object_or_404(FarmRecord, pk=farm_id)
    form = CropExpenseForm(request.POST or None)
    if form.is_valid():
        exp = form.save(commit=False)
        exp.farm_record = farm
        exp.save()
        return redirect('farmrecord_detail', pk=farm_id)
    return render(request, 'expense/expense_form.html', {'form': form, 'farm': farm})
