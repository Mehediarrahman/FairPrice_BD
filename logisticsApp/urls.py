from django.urls import path
from logisticsApp import views
from logisticsApp.views import *

app_name = 'logicticsApp'

urlpatterns = [
    path('', views.logistics_dashboard, name='logistics_dashboard'),
    path('transporters/', views.transporter_list, name='transporter_list'),
    path('transporters/add/', views.add_transporter, name='add_transporter'),
    path('transporters/<int:pk>/edit/', views.edit_transporter, name='edit_transporter'),
    path('trips/', views.trip_list, name='trip_list'),
    path('trips/add/', views.add_trip, name='add_trip'),
    path('analytics/', views.transport_analytics, name='transport_analytics'),
]