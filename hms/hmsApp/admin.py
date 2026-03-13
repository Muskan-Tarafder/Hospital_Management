from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(AvailabilitySlot)
admin.site.register(Booking)
