from django.db import models

class HospitalStatus(models.Model):
    hospital_name = models.CharField(max_length=100, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    available_beds = models.IntegerField()
    icu_beds = models.IntegerField(default=0)
    ventilators = models.IntegerField(default=0)
    remdesivir = models.IntegerField(default=0)
    dexamethasone = models.IntegerField(default=0)
    oxygen_cylinders = models.IntegerField(default=0)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    sos_active = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    sos_latitude = models.FloatField(null=True, blank=True)
    sos_longitude = models.FloatField(null=True, blank=True)
    sos_time=models.DateTimeField(null=True, blank=True)
    sos_place = models.CharField(max_length=255, null=True, blank=True)
    address=models.TextField(null=True, blank=True)
    contact_number=models.CharField(max_length=20, null=True, blank=True)
    

    def __str__(self):
        return self.hospital_name
