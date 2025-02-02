from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.algorithms import GREEDY_COST, optimize
from .models import CurrentFireEvents, Resource
from rest_framework.parsers import FileUploadParser
import csv
import io

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

# API view to upload fire events from a CSV file
@api_view(['POST'])
def upload_fire_events(request):
    """
    Upload fire events from a CSV file
    """
    # Before parsing the CSV file, delete all existing fire events
    CurrentFireEvents.objects.all().delete()

    # Parse the file
    file = request.data['file']
    if not file.name.endswith('.csv'):
        return Response({'error': 'File is not a CSV file'}, status=400)
    data_set = file.read().decode('UTF-8')
    print(file)
    io_string = io.StringIO(data_set)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        _, created = CurrentFireEvents.objects.update_or_create(
            timestamp=column[0],
            fire_start_time=column[1],
            latitude=column[2],
            longitude=column[3],
            severity=column[4]
        )
    return Response({'message': 'Fire events uploaded successfully'}, status=201)


# API view to get all resources in JSON format
@api_view(['GET'])
def get_resources(request):
    """
    Fetch all resources from the database and return as JSON
    """
    resources = Resource.objects.all()
    serializer = ResourceSerializer(resources, many=True)
    return Response(serializer.data)

# API view to upload resources from a json request
@api_view(['POST'])
def upload_resources(request):
    """
    Upload resources from a JSON request
    """
    # Before parsing the JSON file, delete all existing resources
    Resource.objects.all().delete()
    # Parse the JSON file
    data = request.data
    for key, record in data.items():
        Resource.objects.create(
            name=record['name'],
            deployment_time_hr=record['deployment_time_hr'],
            cost_per_operation=record['cost_per_operation'],
            units_available=record['units_available']
        )
    return Response({'message': 'Resources uploaded successfully'}, status=201)


@api_view(['GET'])
def optimize_resources(request):
    """
    Optimize resources for fire events
    """
    # Fetch all fire events from the database
    fire_events = CurrentFireEvents.objects.all()

    # Define algorithm
    algorithm = request.query_params.get('algo', GREEDY_COST)

    return Response(generateReport(fire_events, algorithm))

def generateReport(wildfires, algorithm):
    # Define resources
    resources = Resource.objects.all()

    # Track deployed resources and missed fires
    deployed = []
    missed = []
    operational_cost = 0
    damage_cost = 0

    deployed, missed, operational_cost, damage_cost = optimize(wildfires, resources, algorithm)

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
        },
        'deployed_resources_details': [
            {
            'resource_name': resource.name,
            'deployed_time': resource.assigned_time,
            'location': {
                'latitude': event.latitude,
                'longitude': event.longitude
            }
            } for event, resource in deployed
        ],
        'missed_fires_details': [
            {
            'severity': event.severity,
            'location': {
                'latitude': event.latitude,
                'longitude': event.longitude
            }
            } for event in missed
        ]
    }
    return report
