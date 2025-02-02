from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CurrentFireEvents, Resource

# Serializer for FireEvent model
class FireEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentFireEvents
        fields = ['timestamp', 'fire_start_time', 'latitude', 'longitude', 'severity', 'damage_costs']

# Serializer for Resource model
class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['name', 'deployment_time_hr', 'cost_per_operation', 'units_available']

# API view to get all fire events in JSON format
@api_view(['GET'])
def get_fire_events(request):
    """
    Fetch all fire events from the database and return as JSON
    """
    fire_events = CurrentFireEvents.objects.all()
    serializer = FireEventSerializer(fire_events, many=True)
    return Response(serializer.data)

# API view to get all resources in JSON format
@api_view(['GET'])
def get_resources(request):
    """
    Fetch all resources from the database and return as JSON
    """
    resources = Resource.objects.all()
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)

# Non-API view to optimize resources for fire events
def optimize_resources(request):
    # Fetch all wildfires sorted by severity and start time
    wildfires = CurrentFireEvents.objects.all()

    # Define resources
    resources = {
        'Smoke Jumpers': {'time': 30, 'cost': 5000, 'units': 5},
        'Fire Engines': {'time': 60, 'cost': 2000, 'units': 10},
        'Helicopters': {'time': 45, 'cost': 8000, 'units': 3},
        'Tanker Planes': {'time': 120, 'cost': 15000, 'units': 2},
        'Ground Crews': {'time': 90, 'cost': 3000, 'units': 8},
    }

    # Track deployed resources and missed fires
    deployed = []
    missed = []
    operational_cost = 0
    damage_cost = 0

    for fire in wildfires:
        assigned = False
        for resource, details in resources.items():
            if details['units'] > 0:
                deployed.append((fire, resource))
                operational_cost += details['cost']
                details['units'] -= 1
                assigned = True
                break
        if not assigned:
            missed.append(fire)
            if fire.severity == 'low':
                damage_cost += 50000
            elif fire.severity == 'medium':
                damage_cost += 100000
            elif fire.severity == 'high':
                damage_cost += 200000

    # Generate report
    report = {
        'addressed': len(deployed),
        'missed': len(missed),
        'operational_cost': operational_cost,
        'damage_cost': damage_cost,
        'severity_report': {
            'low': CurrentFireEvents.objects.filter(severity='low').count(),
            'medium': CurrentFireEvents.objects.filter(severity='medium').count(),
            'high': CurrentFireEvents.objects.filter(severity='high').count(),
        }
    }

    return render(request, 'report.html', {'report': report})
