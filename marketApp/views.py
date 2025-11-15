from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import*
from .models import MarketScan, PriceSnapshot
from django.utils import timezone


@login_required
def create_market_scan(request):
    if request.method == "POST":
        form = MarketScanForm(request.POST, request.FILES)
        if form.is_valid():
            scan = form.save(commit=False)
            scan.field_agent = request.user.fieldagent   # FIXED
            scan.save()
            return redirect("market_scan_List")
    else:
        form = MarketScanForm()

    return render(request, "market/market_scan.html", {"form": form})


def market_scan_List(request):
    scans = MarketScan.objects.select_related("product", "region", "field_agent").order_by("-timestamp")
    return render(request, 'market/market_scan_list.html', {"scans": scans})


def create_price_snapshot(request):
    if request.method == "POST":
        form = PriceSnapshotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("price_snapshot_List")
    else:
        form = PriceSnapshotForm()

    return render(request, "market/create_price_snapshot.html", {"form": form})


def price_snapshot_List(request):
    snapshots = PriceSnapshot.objects.select_related("product", "region").order_by("-date")
    return render(request, "market/price_snapshot_List.html", {"snapshots": snapshots})


def Approved(request,id):
    status=PriceSnapshot.objects.get(id=id)
    if status.status == 'Pending':
        status.status='Approved'
    if status.status == 'Approved':
        status.status='Pending'
        
def Rejected(request,id):
    status=PriceSnapshot.objects.get(id=id)
    if status.status == 'Pending':
        status.status='Rejected'
    if status.status == 'Rejected':
        status.status='Pending'
def public_market_portal(request):
    today = timezone.now().date()

    scans = MarketScan.objects.all().order_by("-timestamp")

    
    data = []
    for scan in scans:
        snapshot = PriceSnapshot.objects.filter(
            product=scan.product, 
            region=scan.region, 
            date=today
        ).first()  

        difference = None
        if snapshot:
            difference = scan.observed_price - snapshot.average_price

        data.append({
            "scan": scan,
            "snapshot": snapshot,
            "difference": difference
        })

    return render(request, "market/public_portal.html", {"data": data})