import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Function to process CSV with correct format for MongoDB
def process_csv(uploaded_file, is_environmental=False, is_current_wildfire=False):
    """Reads and processes CSV to match MongoDB format."""
    
    # Read CSV
    df = pd.read_csv(uploaded_file)

    # Convert timestamp & fire_start_time to correct format
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df["fire_start_time"] = pd.to_datetime(df["fire_start_time"]).dt.strftime("%Y-%m-%d %H:%M:%S")

    if is_current_wildfire:
        # ✅ Split 'location' column into 'latitude' and 'longitude'
        df[['latitude', 'longitude']] = df['location'].str.split(',', expand=True)

        # ✅ Convert latitude & longitude to float
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)

        # ✅ Drop the original 'location' column
        df.drop(columns=['location'], inplace=True)

    elif not is_environmental:
        # ✅ Convert latitude & longitude to correct format for historical wildfire
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)

    else:
        # ✅ Convert environmental data correctly
        numeric_cols = ["temperature", "humidity", "wind_speed", "precipitation", "vegetation_index", "human_activity_index", "latitude", "longitude"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # ✅ Ensure exact field ordering (excluding the 'id' column, since MongoDB generates it)
    ordered_columns = ["timestamp", "fire_start_time", "latitude", "longitude", "severity"]
    df = df[ordered_columns] if not is_environmental else df

    return df

# Streamlit UI
def show():
    """Streamlit UI for file upload and testing data processing."""

    st.title("🚀 SAP Wildfire Management Service - Test Data Processing")

    uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

    # Dropdown for data selection
    options = {
        "Current Wildfire": ("backend_currentfireevents", False, True),
        "Historical Wildfire": ("backend_historicalfireevents", False, False),
        "Historical Environmental Data": ("backend_historicalenvironmentaldata", True, False),
        "Future Environmental Data": ("backend_futureenvironmentaldata", True, False)
    }
    
    selected_option = st.selectbox("📊 Select Data Type", list(options.keys()), index=None, placeholder="Choose an option...")

    if uploaded_file and selected_option:
        collection_name, is_environmental, is_current_wildfire = options[selected_option]

        if st.button("🔍 Test Processing"):
            df = process_csv(uploaded_file, is_environmental, is_current_wildfire)

            st.write("📋 **Preview Data Before Uploading**")
            st.dataframe(df.head(10))  

            st.write("📝 **Strict MongoDB JSON Format**")
            sample_data = json.dumps(df.head(5).to_dict(orient="records"), indent=4)
            st.code(sample_data, language="json")

            st.success("✅ Data is correctly formatted and ready for MongoDB.")
