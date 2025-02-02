import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Caching the CSV loading function for performance
@st.cache
def load_csv(csv_file_path):
    try:
        df = pd.read_csv(csv_file_path)
        return df
    except Exception as e:
        st.error(f"Error loading CSV: {e}")
        return None

def show():
    st.title("🌿 Part 2: Environmental Analysis")

    # Path to the CSV file
    csv_file_path = "C:\\Users\\Mahmu\\ConUHacksSAP\\ConUHacksSAPdjango\\predicted_wildfire_occurrences_with_location.csv"

    # Step 1: Load the CSV data using caching
    df = load_csv(csv_file_path)

    # If CSV failed to load, return
    if df is None:
        return

    # Check if the necessary columns (latitude and longitude) exist
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        st.error("CSV must contain 'latitude' and 'longitude' columns.")
        return

    # Step 2: Filter data for performance (e.g., showing only the first 100 rows)
    # You can use a slider to allow users to load only a portion of data.
    rows_to_display = st.slider("Select the number of rows to display", 10, len(df), 100)
    df_subset = df.head(rows_to_display)

    # Step 3: Create a Folium map centered on the first coordinate pair
    m = folium.Map(location=[df_subset['latitude'].iloc[0], df_subset['longitude'].iloc[0]], zoom_start=10)

    # Step 4: Add a marker (pin) for each row in the filtered CSV data
    for _, row in df_subset.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        predicted_fire = row['predicted_fire']

        # If 'predicted_fire' is 1, color the marker in red (for predicted fire)
        marker_color = 'red' if predicted_fire == 1 else 'green'

        # Add marker with popup information
        folium.Marker(
            location=[lat, lon],
            popup=f"Timestamp: {row['timestamp']}<br>Predicted Fire: {'Yes' if predicted_fire == 1 else 'No'}",
            icon=folium.Icon(color=marker_color, icon="info-sign")
        ).add_to(m)

    # Step 5: Set up the layout and make the map full-screen
    st.write("### Map with Predicted Fires")

    # Use CSS to make the map container full-screen
    st.markdown(
        """
        <style>
            .stApp {
                padding: 0 !important;
                margin: 0 !important;
            }
            .st-folium {
                height: 100vh !important;
                width: 100vw !important;
                margin: 0 !important;
                padding: 0 !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Display the map with full-screen size
    st_folium(m, height=900, width="100%")  # Adjust height and width as needed
