from django.urls import path
from . import views

urlpatterns = [

    # Farmer
    path('farmer/', views.farmer_list, name='farmer_list'),
    path('farmer/create/', views.farmer_create, name='farmer_create'),
    path('farmer/edit/<int:pk>/', views.farmer_edit, name='farmer_edit'),
    path('farmer/delete/<int:pk>/', views.farmer_delete, name='farmer_delete'),

    # Crop
    path('crop/', views.crop_list, name='crop_list'),
    path('crop/create/', views.crop_create, name='crop_create'),
    path('crop/edit/<int:pk>/', views.crop_edit, name='crop_edit'),
    path('crop/delete/<int:pk>/', views.crop_delete, name='crop_delete'),

    # FarmRecord
    path('farmrecord/', views.farmrecord_list, name='farmrecord_list'),
    path('farmrecord/create/', views.farmrecord_create, name='farmrecord_create'),
    path('farmrecord/edit/<int:pk>/', views.farmrecord_edit, name='farmrecord_edit'),
    path('farmrecord/delete/<int:pk>/', views.farmrecord_delete, name='farmrecord_delete'),
    path('farmrecord/detail/<int:pk>/', views.farmrecord_detail, name='farmrecord_detail'),

    # Expense
    path('expense/create/<int:farm_id>/', views.expense_create, name='expense_create'),
]
