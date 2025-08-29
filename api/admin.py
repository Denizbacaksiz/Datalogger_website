from django.contrib import admin
from .models import Device, DeviceReading
from django.utils.translation import gettext_lazy as _

# Admin panel başlığı ve site adı
admin.site.site_title = _("Datalogger Admin")
admin.site.site_header = _("Datalogger Admin Panel")
admin.site.index_title = _("Admin İşlemleri")


admin.site.register(Device)
admin.site.register(DeviceReading)