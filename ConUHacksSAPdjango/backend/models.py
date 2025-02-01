from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=50)
    deployment_time_hr = models.DecimalField(decimal_places=2,max_digits=4)
    cost_per_operation = models.DecimalField(decimal_places=2, max_digits=10)
    units_available = models.IntegerField()

    def __str__(self):
        return self.name

# Create instances of the Resource model for each type of resource
resources = [
    {"name": "Smoke Jumpers", "deployment_time_hr": 0.5, "cost_per_operation": 5000, "units_available": 5},
    {"name": "Fire Engines", "deployment_time_hr": 1.0, "cost_per_operation": 2000, "units_available": 10},
    {"name": "Helicopters", "deployment_time_hr": 0.75, "cost_per_operation": 8000, "units_available": 3},
    {"name": "Tanker Planes", "deployment_time_hr": 2.0, "cost_per_operation": 15000, "units_available": 2},
    {"name": "Ground Crews", "deployment_time_hr": 1.5, "cost_per_operation": 3000, "units_available": 8},
]

for resource in resources:
    Resource.objects.create(**resource)



# Create your models here.
class CurrentFireEvents(models.Model):
    timestamp = models.DateTimeField()
    fire_start_time = models.DateTimeField()
    latitude = models.DecimalField(decimal_places=6, max_digits=10, default=0)
    longitude = models.DecimalField(decimal_places=6, max_digits=10,default=0)

    severity = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    @property
    def damage_costs(self):
        if self.severity == 'low':
            return 50000
        elif self.severity == 'medium':
            return 100000
        elif self.severity == 'high':
            return 200000
        return -1

    def __str__(self):
        return f"{self.timestamp} - {self.severity}"
