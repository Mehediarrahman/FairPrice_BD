from django.urls import path
from farmarApp.views import*

urlpatterns = [

    # Farmer
    path('farmer/',farmer_list, name='farmer_list'),
    path('farmer/create/',farmer_create, name='farmer_create'),
    path('farmer/edit/<int:pk>/', farmer_edit, name='farmer_edit'),
    path('farmer/delete/<int:pk>/', farmer_delete, name='farmer_delete'),

    # Crop
    path('crop/', crop_list, name='crop_list'),
    path('crop/create/', crop_create, name='crop_create'),
    path('crop/edit/<int:pk>/',crop_edit, name='crop_edit'),
    path('crop/delete/<int:pk>/',crop_delete, name='crop_delete'),

    # FarmRecord
    path('farmrecord/',farmrecord_list, name='farmrecord_list'),
    path('farmrecord/create/',farmrecord_create, name='farmrecord_create'),
    path('farmrecord/edit/<int:pk>/', farmrecord_edit, name='farmrecord_edit'),
    path('farmrecord/delete/<int:pk>/',farmrecord_delete, name='farmrecord_delete'),
    path('farmrecord/detail/<int:pk>/', farmrecord_detail, name='farmrecord_detail'),

    # Expense
    path('expense/create/<int:farm_id>/', expense_create, name='expense_create'),
]
