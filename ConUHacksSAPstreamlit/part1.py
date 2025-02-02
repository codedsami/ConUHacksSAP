import pandas as pd
import streamlit as st
import folium
import requests
from datetime import datetime
from streamlit_folium import st_folium

# Define the Django backend API URL
optimize_url = "http://localhost:8000/api/optimize/"
fire_events_url = "http://localhost:8000/api/fire_events/"
save_file_url = "http://localhost:8000/api/upload/fire_events/"
save_resources_url = "http://localhost:8000/api/allocate/resources/"
sj = {"name": "Smoke Jumpers", "deployment_time_hr": 0.5, "cost": 5000}
fe = {"name": "Fire Engines", "deployment_time_hr": 1, "cost": 2000}
h = {"name": "Helicopters", "deployment_time_hr": 0.75, "cost": 8000}
tp = {"name": "Tanker Planes", "deployment_time_hr": 2, "cost": 15000}
gc = {"name": "Ground Crews", "deployment_time_hr": 1.5, "cost": 3000}

def show():
    st.title("🔥 Wildfire Tracker")
    # # add file uploader .csv
    # st.write("Upload a CSV file with wildfire data")
    # uploaded_file = st.file_uploader("Choose a file")
    # # save it temporarily for later use
    # if uploaded_file is not None:
    #     # make sure the file is a CSV
    #     if uploaded_file.name.split(".")[-1] != "csv":
    #         st.error("Please upload a CSV file")
    #         return
    #     a = pd.read_csv(uploaded_file)
    #     st.success("File uploaded successfully", icon="✅")
    # # backend POST API call to save the file
    # # show resources selection
    # st.write("Select the resources to allocate for the wildfire:")
    # response={}
    # # show counter +/- for resources: Smoke Jumpers, Fire Engines, Helicopters, Tanker Planes, Firefighters
    # smoke_jumpers = st.number_input("Smoke Jumpers 🪂 (30 mins, $5,000)", min_value=0, value=0)
    # fire_engines = st.number_input("Fire Engines 🚒 (1 hour, $2,000)", min_value=0, value=0)
    # helicopters = st.number_input("Helicopters 🚁 (45 mins, $8,000)", min_value=0, value=0)
    # tanker_planes = st.number_input("Tanker Planes ✈️ (2 hours, $15,000)", min_value=0, value=0)
    # ground_crews = st.number_input("Ground Crews 👨‍🚒 (1.5 hours, $3,000)", min_value=0, value=0)
    # # show submit button
    # if st.button("Submit"):
    #     if uploaded_file is None:
    #         st.error("Please upload a CSV file before submitting")
    #         return
    #     requests.post(save_file_url, files={"file": a})
    #     # backend POST API call to allocate resources
    #     # for i in range(smoke_jumpers):
    #     #     response = requests.post(save_resources_url, json=sj)
    #     # for i in range(fire_engines):
    #     #     response = requests.post(save_resources_url, json=fe)
    #     # for i in range(helicopters):
    #     #     response = requests.post(save_resources_url, json=h)
    #     # for i in range(tanker_planes):
    #     #     response = requests.post(save_resources_url, json=tp)
    #     # for i in range(ground_crews):
    #     #     response = requests.post(save_resources_url, json=gc)
    #     st.write("Resources allocated successfully")
    #     # once resources are allocated, show the map and hide everything else
    display_map()

    


def display_map():
    if 'optimized' not in st.session_state:
        st.session_state.optimized = requests.get(optimize_url).json()
    optimized = st.session_state.optimized

    m = folium.Map(location=[45.7747, -73.3052], zoom_start=8)
    # Show information about the optimization
    st.write(f"**Optimization Results**")
    st.write(f"**Number of fires addressed:** {optimized['addressed']}")
    st.write(f"**Number of fires missed:** {optimized['missed']}")
    st.write(f"**Total operational cost:** ${optimized['operational_cost']}")
    st.write(f"**Total damage cost:** ${optimized['damage_cost']}")
    st.write(f"**Severity Report:**")
    st.write(f"- Low severity fires: {optimized['severity_report']['low']}")
    st.write(f"- Medium severity fires: {optimized['severity_report']['medium']}")
    st.write(f"- High severity fires: {optimized['severity_report']['high']}")


    # **🔥 Step 5: Loop Through Fire Events and Display Correct Markers**
    # for fire in fire_events:
    #     fire_time = datetime.strptime(fire["fire_start_time"], "%Y-%m-%d %H:%M")
    #     reported_time = datetime.strptime(fire["timestamp"], "%Y-%m-%d %H:%M") if fire.get("timestamp") else None
    #     location = [fire['latitude'], fire['longitude']]

    #     severity = fire["severity"].lower()  # Ensure severity is in lowercase
    #     color = {"high": "red", "medium": "orange", "low": "pink"}.get(severity, "blue")
    #     folium.Marker(
    #         location=location,
    #         popup=f"""
    #         <table>
    #         <tr><td><b>Estimated Start:</b></td><td>{fire['fire_start_time']}</td></tr>
    #         <tr><td><b>Reported Time:</b></td><td>{reported_time if reported_time else 'N/A'}</td></tr>
    #         <tr><td><b>Severity:</b></td><td>{fire['severity'].upper()}</td></tr>
    #         </table>
    #         """,
    #         icon=folium.Icon(color=color, icon="info-sign")
    #     ).add_to(m)

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

    # **🔥 Step 6: Render the Full-Screen Map**
    st_folium(m, width=1000, height=500)
