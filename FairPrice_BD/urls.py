
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("market/", include("marketApp.urls")),
    path('logisticsApp/', include('logicticsApp.urls')),

]