from django.db import models


class Resource(models.Model):
    name = models.CharField(max_length=50)
    deployment_time_hr = models.DecimalField(decimal_places=2,max_digits=4)
    cost_per_operation = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return self.name

class CurrentFireEvents(models.Model):
    timestamp = models.DateTimeField()
    fire_start_time = models.DateTimeField()
    latitude = models.DecimalField(decimal_places=6, max_digits=10, default=0)
    longitude = models.DecimalField(decimal_places=6, max_digits=10,default=0)
    severity = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    @property
    def damage_costs(self):
        severity_costs = {
            'low': 50000,
            'medium': 100000,
            'high': 200000
        }
        return severity_costs.get(self.severity, 0)

    def __str__(self):
        return f"Timestamp: {self.timestamp}, Fire Start Time: {self.fire_start_time}, Latitude: {self.latitude}, Longitude: {self.longitude}, Severity: {self.severity}, Damage Costs: {self.damage_costs}"

class HistoricalEnvironmentalData(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.DecimalField(decimal_places=2, max_digits=5)
    humidity = models.DecimalField(decimal_places=2, max_digits=5)
    wind_speed = models.DecimalField(decimal_places=2, max_digits=5)
    precipitation = models.DecimalField(decimal_places=2, max_digits=5)
    vegetation_index = models.DecimalField(decimal_places=2, max_digits=5)
    human_activity_index = models.DecimalField(decimal_places=2, max_digits=5)
    latitude = models.DecimalField(decimal_places=6, max_digits=10, default=0)
    longitude = models.DecimalField(decimal_places=6, max_digits=10,default=0)

    def __str__(self):
        return f"{self.timestamp} - Temp: {self.temperature}°C, Humidity: {self.humidity}%, Wind Speed: {self.wind_speed} m/s, Precipitation: {self.precipitation} mm, Vegetation Index: {self.vegetation_index}, Human Activity Index: {self.human_activity_index}, Location: ({self.latitude}, {self.longitude})"


class HistoricalFireEvents(models.Model):
    timestamp = models.DateTimeField()
    fire_start_time = models.DateTimeField()
    latitude = models.DecimalField(decimal_places=6, max_digits=10, default=0)
    longitude = models.DecimalField(decimal_places=6, max_digits=10,default=0)
    severity = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')])

    def __str__(self):
     return f"{self.timestamp} - {self.fire_start_time} - {self.latitude}, {self.longitude} - {self.severity}"

class FutureEnvironmentalData(models.Model):
    timestamp = models.DateTimeField()
    temperature = models.DecimalField(decimal_places=2, max_digits=5)
    humidity = models.DecimalField(decimal_places=2, max_digits=5)
    wind_speed = models.DecimalField(decimal_places=2, max_digits=5)
    precipitation = models.DecimalField(decimal_places=2, max_digits=5)
    vegetation_index = models.DecimalField(decimal_places=2, max_digits=5)
    human_activity_index = models.DecimalField(decimal_places=2, max_digits=5)
    latitude = models.DecimalField(decimal_places=6, max_digits=10, default=0)
    longitude = models.DecimalField(decimal_places=6, max_digits=10,default=0)

    def __str__(self):
        return f"{self.timestamp} - Temp: {self.temperature}°C, Humidity: {self.humidity}%, Wind Speed: {self.wind_speed} m/s, Precipitation: {self.precipitation} mm, Vegetation Index: {self.vegetation_index}, Human Activity Index: {self.human_activity_index}, Location: ({self.latitude}, {self.longitude})"
