"""
URL configuration for Staj_2025 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import *




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home_view, name='home'),
    path('device/<str:device_id>/', device_detail_view, name='device_detail'),
    path('compare_devices',compare_devices_view, name='compare_devices'),


    path('api/device/add_device/', add_device, name='add_device'),
    path('api/device/<str:device_id>/add_data/', add_data, name='add_data'),
    path('api/device/<str:device_id>/update_data/', update_data, name='update_data'),
    path('api/device/<str:device_id>/delete_data/', delete_data, name='delete_data'),
    path('api/device/<str:device_id>/delete_device/', delete_device, name='delete_device'),
]
