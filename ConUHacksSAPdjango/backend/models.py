from django.db import models

# Create your models here.
class CurrentFireEvents(models.Model):
    timestamp = models.DateTimeField()
    fire_start_time = models.DateTimeField()
    latitude = models.DecimalField(decimal_places=6, max_digits=10, default=0)
    longitude = models.DecimalField(decimal_places=6, max_digits=10,default=0)

    severity = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    def __str__(self):
        return f"{self.timestamp} - {self.severity}"
