from django.urls import path
from warehouseApp.views import*

urlpatterns = [
    # Warehouse
    path('warehouses/', warehouse_list, name='warehouse_list'),
    path('warehouses/add/',warehouse_create, name='warehouse_create'),
    path('warehouses/<int:pk>/edit/',warehouse_edit, name='warehouse_edit'),
    path('warehouses/<int:pk>/delete/',warehouse_delete, name='warehouse_delete'),

    # Warehouse Cost
    path('warehouse-costs/',warehouse_cost_list, name='warehouse_cost_list'),
    path('warehouse-costs/add/', warehouse_cost_create, name='warehouse_cost_create'),
    path('warehouse-costs/<int:pk>/edit/', warehouse_cost_edit, name='warehouse_cost_edit'),
    path('warehouse-costs/<int:pk>/delete/',warehouse_cost_delete, name='warehouse_cost_delete'),

    # Calculation (Average Storage Cost Per Ton)
    path('warehouse-cost-summary/',warehouse_cost_summary, name='warehouse_cost_summary'),
]
