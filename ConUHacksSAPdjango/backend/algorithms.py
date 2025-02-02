from collections import Counter
from datetime import datetime

# Greedy algorithm: lowest cost first
GREEDY_COST = "GREEDY_COST"
GREEDY_TIME = "GREEDY_TIME"
GREEDY_UNITS = "GREEDY_UNITS"

def greedy(wildfires, resources):
    deployed = []
    missed = []
    operational_cost = 0
    damage_cost = 0
    # add 2 more fields to the resource model. temporarily for calculation purposes
    for resource in resources:
        resource.assigned_time = None
        resource.assigned = False


    for fire in wildfires:
        assigned = False
        for resource in resources:
            if resource.assigned and (datetime.strptime(fire.timestamp, '%Y-%m-%d %H:%M') - datetime.strptime(resource.assigned_time, '%Y-%m-%d %H:%M')).total_seconds() / 3600 >= resource.deployment_time_hr:
                resource.assigned = False
            if resource.assigned == False:
                deployed.append((fire, resource))
                operational_cost += float(str(resource.cost_per_operation))
                # start a timer for the resource to make it available again after deployment_time_hr
                resource.assigned_time = fire.timestamp
                resource.assigned = True
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
    return deployed, missed, operational_cost, damage_cost


# implementation of the greedy algorithm

def optimize(wildfires, resources, algorithm):
    wildfires = sorted(wildfires, key=lambda x: (x.timestamp))
    if algorithm == GREEDY_COST:
        resources = sorted(resources, key=lambda x: float(str(x.cost_per_operation)))
        return greedy(wildfires, resources)
    elif algorithm == GREEDY_TIME:
        resources = sorted(resources, key=lambda x: float((x.deployment_time_hr)))
        return greedy(wildfires, resources)
    elif algorithm == GREEDY_UNITS:
        resource_counts = Counter([resource.name for resource in resources])
        resources = sorted(resources, key=lambda x: (-resource_counts[x.name], x.name))
        return greedy(wildfires, resources)
    else:
        raise ValueError(f"Invalid algorithm: {algorithm}")

