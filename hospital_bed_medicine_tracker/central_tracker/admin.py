from django.contrib import admin
from .models import HospitalStatus

@admin.register(HospitalStatus)
class HospitalStatusAdmin(admin.ModelAdmin):
    list_display = (
        'hospital_name',
        'available_beds',
        'sos_active',
        'last_updated'
    )
