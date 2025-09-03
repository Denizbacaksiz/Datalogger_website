from django.db import models



class Device(models.Model):
    name = models.CharField(max_length=100, default="")
    device_id = models.CharField(max_length=100, unique=True, null = False, default=None, blank=False)

    def latest_reading(self):
        return self.readings.order_by('-created_at').first()

    def __str__(self):
        return self.name



class DeviceReading(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE,related_name='readings')
    properties = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']


    @property
    def data(self):
        return self.properties

    @property
    def timestamp(self):
        return self.created_at

    def __str__(self):
        return self.device.name
