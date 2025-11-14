from django.urls import path
from marketApp.views import*

urlpatterns = [
    path("market_scan/", create_market_scan, name="market_scan"),
    path("market_scan_List/", market_scan_List, name="market_scan_List"),
    path("price_snapshot/", create_price_snapshot, name="price_snapshot"),
    path("price_snapshot_List/", price_snapshot_List, name="price_snapshot_List"),
    path("public_market_portal/", public_market_portal, name="public_market_portal"),
    path("Rejected/<int:id>", Rejected, name="Rejected"),
    path("Approved/<int:id>", Approved, name="Approved"),

]
