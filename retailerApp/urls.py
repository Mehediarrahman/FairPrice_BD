from django.urls import path
from . import views

app_name = 'retailerApp'

urlpatterns = [
    path('dashboard/', views.retailer_dashboard, name='retailer_dashboard'),
    path('profile/create/', views.create_retailer_profile, name='create_retailer_profile'),
    path('profile/update/', views.update_retailer_profile, name='update_retailer_profile'),
    path('products/', views.product_list, name='product_list'),
    path('product-price/create/', views.create_product_price, name='create_product_price'),
    path('product-price/update/<int:pk>/', views.update_product_price, name='update_product_price'),
    path('product-price/delete/<int:pk>/', views.delete_product_price, name='delete_product_price'),
    path('ajax/load-products/', views.load_products, name='ajax_load_products'),


    
]