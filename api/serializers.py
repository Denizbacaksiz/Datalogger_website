from rest_framework import serializers
from .models import Device,DeviceReading

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ['device_id','properties','created_at','updated_at','is_active']

class DeviceReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReading
        fields = ['device_id','properties','created_at','updated_at','is_active']