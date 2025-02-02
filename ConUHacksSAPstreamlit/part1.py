import streamlit as st
import folium
import pymongo
from folium.plugins import TimestampedGeoJson
from datetime import datetime
import json

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["wildfire_db"]  # Replace with your database name
collection = db["wildfires"]  # Replace with your collection name

# Fetch data from MongoDB
fires_data = collection.find()

# Convert the fetched data into a list
fire_list = list(fires_data)

# Function to determine color based on severity
def severity_color(severity):
    if severity == "high":
        return "red"
    elif severity == "medium":
        return "orange"
    else:
        return "blue"

# Convert the data into a GeoJSON-like format for the map
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for fire in fire_list:
    # Convert fire_start_time to datetime
    fire_start_time = datetime.strptime(fire["fire_start_time"], "%Y-%m-%d %H:%M")
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [fire["longitude"], fire["latitude"]],
        },
        "properties": {
            "timestamp": fire_start_time.isoformat(),
            "severity": fire["severity"],
            "emoji": "🔥",
            "fire_start_time": fire_start_time.isoformat(),
        },
    }
    geojson_data["features"].append(feature)

# Create Streamlit map
m = folium.Map(location=[45.7747, -73.3052], zoom_start=12)

# Add the fire locations to the map as markers
for fire in fire_list:
    severity = fire["severity"]
    color = severity_color(severity)

    folium.Marker(
        location=[fire["latitude"], fire["longitude"]],
        popup=f"Fire started at {fire['fire_start_time']} | Severity: {fire['severity']}",
        icon=folium.Icon(color=color, icon="info-sign"),
    ).add_to(m)

# Add TimestampedGeoJson for interactive timeline
timestamped_geojson = TimestampedGeoJson(
    geojson_data,
    period="PT1H",  # 1 hour per timestamp (can be adjusted)
    add_last_point=True,
).add_to(m)

# Display map in Streamlit
st.write("### Wildfire Map Visualization")
st.map(m)

# Time filter slider
start_time = datetime.strptime(fire_list[0]["fire_start_time"], "%Y-%m-%d %H:%M")
end_time = datetime.strptime(fire_list[-1]["fire_start_time"], "%Y-%m-%d %H:%M")
selected_time = st.slider("Select time range", 
                          min_value=start_time, 
                          max_value=end_time, 
                          value=(start_time, end_time), 
                          format="YYYY-MM-DD HH:mm")

# Filter the data based on the selected time range
filtered_fires = [fire for fire in fire_list if selected_time[0] <= datetime.strptime(fire["fire_start_time"], "%Y-%m-%d %H:%M") <= selected_time[1]]

# Update the map with filtered data
filtered_geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for fire in filtered_fires:
    fire_start_time = datetime.strptime(fire["fire_start_time"], "%Y-%m-%d %H:%M")
    
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [fire["longitude"], fire["latitude"]],
        },
        "properties": {
            "timestamp": fire_start_time.isoformat(),
            "severity": fire["severity"],
            "emoji": "🔥",
            "fire_start_time": fire_start_time.isoformat(),
        },
    }
    filtered_geojson_data["features"].append(feature)

# Add TimestampedGeoJson for the filtered data
timestamped_geojson = TimestampedGeoJson(
    filtered_geojson_data,
    period="PT1H",
    add_last_point=True,
).add_to(m)

# Display the filtered map in Streamlit
st.write(f"### Filtered Wildfire Map for the selected time range ({selected_time[0]} to {selected_time[1]})")
st.map(m)
