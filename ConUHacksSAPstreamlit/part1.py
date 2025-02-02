import streamlit as st
import folium
import requests
from datetime import datetime
from streamlit_folium import st_folium

# Define the Django backend API URL
fire_events_url = "http://localhost:8000/api/fire_events/"

def show():
    st.title("🔥 Wildfire Tracker")

    # **🔥 Step 1: Load Data ONCE (for smooth slider performance)**
    if "fire_events" not in st.session_state:
        response = requests.get(fire_events_url)
        if response.status_code == 200:
            st.session_state.fire_events = response.json()
        else:
            st.error("Failed to fetch fire events data")
            return

    fire_events = st.session_state.fire_events  # Use preloaded data

    if not fire_events:
        st.warning("No fire events found.")
        return

    # **🔥 Step 2: Extract Fire Start and Reported Times**
    fire_start_times = [datetime.strptime(fire["fire_start_time"], "%Y-%m-%d %H:%M") for fire in fire_events]
    reported_times = [datetime.strptime(fire["reported_time"], "%Y-%m-%d %H:%M") for fire in fire_events if fire.get("reported_time")]

    start_time = min(fire_start_times)
    end_time = max(reported_times) if reported_times else max(fire_start_times)

    if start_time == end_time:
        st.warning("All fire events have the same start and reported time. No valid timeline filtering possible.")
        return

    # **🔥 Step 3: Timeline Slider**
    selected_time = st.slider("Select fire timeline",
                              min_value=start_time, 
                              max_value=end_time, 
                              value=start_time, 
                              format="YYYY-MM-DD")

    # **🔥 Step 4: Keep Map Static & Only Update Markers**
    m = folium.Map(location=[45.7747, -73.3052], zoom_start=6)

    # **🔥 Step 5: Loop Through Fire Events and Display Correct Markers**
    for fire in fire_events:
        fire_time = datetime.strptime(fire["fire_start_time"], "%Y-%m-%d %H:%M")
        reported_time = datetime.strptime(fire["reported_time"], "%Y-%m-%d %H:%M") if fire.get("reported_time") else None
        location = [fire['latitude'], fire['longitude']]

        if fire_time <= selected_time:
            # **📍 Show colored pin based on severity**
            severity = fire["severity"].lower()  # Ensure severity is in lowercase
            color = {"high": "red", "medium": "orange", "low": "pink"}.get(severity, "blue")
            folium.Marker(
                location=location,
                popup=f"<b>Fire Reported:</b> {reported_time if reported_time else fire['fire_start_time']} <br> Severity: {fire['severity']}",
                icon=folium.Icon(color=color, icon="info-sign")
            ).add_to(m)

    # **🔥 Step 6: Render the Full-Screen Map**
    st_folium(m, height=800, width=1600)  # Increased size for full-screen effect
