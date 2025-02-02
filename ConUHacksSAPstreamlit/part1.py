import streamlit as st
import folium
import requests
from datetime import datetime
from streamlit_folium import st_folium

# Define the Django backend API URLs
optimize_url = "http://localhost:8000/api/optimize/"
fire_events_url = "http://localhost:8000/api/fire_events/"

# Resource details (for reference)
sj = {"name": "Smoke Jumpers", "deployment_time_hr": 0.5, "cost": 5000}
fe = {"name": "Fire Engines", "deployment_time_hr": 1, "cost": 2000}
h = {"name": "Helicopters", "deployment_time_hr": 0.75, "cost": 8000}
tp = {"name": "Tanker Planes", "deployment_time_hr": 2, "cost": 15000}
gc = {"name": "Ground Crews", "deployment_time_hr": 1.5, "cost": 3000}

def display_map():
    """Display the optimization results map."""
    if 'optimized' not in st.session_state:
        try:
            response = requests.get(optimize_url)
            response.raise_for_status()  # Raise an error for bad status codes
            st.session_state.optimized = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch optimization data: {e}")
            return

    optimized = st.session_state.optimized

    # Create a folium map centered on a default location
    m = folium.Map(location=[45.7747, -73.3052], zoom_start=8)

    # Show information about the optimization
    st.write("**Optimization Results**")
    st.write(f"**Number of fires addressed:** {optimized['addressed']}")
    st.write(f"**Number of fires missed:** {optimized['missed']}")
    st.write(f"**Total operational cost:** ${optimized['operational_cost']}")
    st.write(f"**Total damage cost:** ${optimized['damage_cost']}")
    st.write("**Severity Report:**")
    st.write(f"- Low severity fires: {optimized['severity_report']['low']}")
    st.write(f"- Medium severity fires: {optimized['severity_report']['medium']}")
    st.write(f"- High severity fires: {optimized['severity_report']['high']}")

    # Deployed resources markers
    deployed_resources = optimized.get("deployed_resources_details", [])
    for resource in deployed_resources:
        location = [resource["location"]["latitude"], resource["location"]["longitude"]]
        deployed_time = datetime.strptime(resource["deployed_time"], "%Y-%m-%d %H:%M")
        folium.Marker(
            location=location,
            popup=f"""
            <table>
            <tr><td><b>Resource:</b></td><td>{resource['resource_name']}</td></tr>
            <tr><td><b>Deployed Time:</b></td><td>{deployed_time}</td></tr>
            </table>
            """,
            icon=folium.Icon(color="green", icon="info-sign")
        ).add_to(m)
    
    # Missed fires markers
    missed_fires = optimized.get("missed_fires", [])
    for fire in missed_fires:
        location = [fire["latitude"], fire["longitude"]]
        folium.Marker(
            location=location,
            popup=f"""
            <table>
            <tr><td><b>Estimated Start:</b></td><td>{fire['fire_start_time']}</td></tr>
            <tr><td><b>Severity:</b></td><td>{fire['severity'].upper()}</td></tr>
            </table>
            """,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

    # Render the map with unique key for the first map
    st_folium(m, width="100%", height=500, key="opt_map")

def display_fire_slider_map():
    """Display the fire events map with a time slider."""
    if 'fire_events' not in st.session_state:
        try:
            response = requests.get(fire_events_url)
            response.raise_for_status()  # Raise an error for bad status codes
            st.session_state.fire_events = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to fetch fire events data: {e}")
            return

    fire_events = st.session_state.fire_events

    if not fire_events:
        st.error("No fire events found.")
        return

    # Step 1: Create a slider to filter fire events based on time
    timestamps = [fire["fire_start_time"] for fire in fire_events]
    timestamps = [datetime.strptime(ts, "%Y-%m-%d %H:%M") for ts in timestamps]
    min_time = min(timestamps)
    max_time = max(timestamps)

    selected_time = st.slider(
        "Select fire start time",
        min_value=min_time,
        max_value=max_time,
        value=min_time,
        format="YYYY-MM-DD HH:mm",
        key="fire_slider"  # Unique key for the slider
    )

    # Step 2: Create the second map
    fire_map = folium.Map(location=[fire_events[0]["latitude"], fire_events[0]["longitude"]], zoom_start=8)

    # Step 3: Add markers to the map based on the selected time
    for fire in fire_events:
        fire_time = datetime.strptime(fire["fire_start_time"], "%Y-%m-%d %H:%M")
        if fire_time <= selected_time:
            severity = fire["severity"].lower()
            color = {"high": "red", "medium": "orange", "low": "pink"}.get(severity, "blue")
            folium.Marker(
                location=[fire["latitude"], fire["longitude"]],
                popup=f"Start Time: {fire['fire_start_time']} | Severity: {fire['severity']}",
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(fire_map)

    # Display the second map with a unique key
    st.write("### Fire Events with Time Filter")
    st_folium(fire_map, width="100%", height=500, key="fire_map")  # Unique key for the second map

def show():
    """Main function to display the app."""
    st.title("🔥 Wildfire Tracker")

    display_map()  # Display the optimization results map
    display_fire_slider_map()  # Display the fire events map with a time slider

# Run the app
try:
    show()
except Exception as e:
    st.error(f"An error occurred: {e}")
