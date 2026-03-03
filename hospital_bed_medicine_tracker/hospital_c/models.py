from django.db import models

class Resource(models.Model):
    RESOURCE_TYPE = (
        ('BED', 'Bed'),
        ('MEDICINE', 'Medicine'),
        ('EQUIPMENT', 'Equipment'),
    )

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=RESOURCE_TYPE)
    available_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
