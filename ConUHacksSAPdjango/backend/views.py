from django.shortcuts import render
from backend.models import CurrentFireEvents

def optimize_resources(request):
    # Fetch all wildfires sorted by severity and start time
    wildfires = CurrentFireEvents.objects.all().order_by('-severity', 'fire_start_time')

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
