import streamlit as st
import pandas as pd
from datetime import datetime
import json
from pymongo import MongoClient

# **🔥 Step 1: Connect to MongoDB**
MONGO_URI = "mongodb://localhost:27017/"  # Change if using a remote DB
DB_NAME = "mydatabase"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# **🔥 Function to Process CSV & Convert to MongoDB Format**
def process_csv(uploaded_file, is_environmental=False, is_current_wildfire=False):
    """Reads and processes CSV to match MongoDB format."""
    df = pd.read_csv(uploaded_file, dtype=str)

    # ✅ Handle multiple timestamp formats
    def parse_datetime(dt):
        possible_formats = [
            "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%d %I:%M %p", "%Y-%m-%d %I:%M:%S %p"
        ]
        for fmt in possible_formats:
            try:
                return datetime.strptime(dt.strip(), fmt).strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                continue
        st.warning(f"⚠️ Unrecognized timestamp format: {dt}")
        return None  

    # ✅ Apply timestamp formatting
    df["timestamp"] = df["timestamp"].apply(parse_datetime)
    if "fire_start_time" in df.columns:
        df["fire_start_time"] = df["fire_start_time"].apply(parse_datetime)

    # ✅ Process Data Based on Type
    if is_current_wildfire:
        df[['latitude', 'longitude']] = df['location'].str.split(',', expand=True)
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)
        df.drop(columns=['location'], inplace=True)
    elif not is_environmental:
        df["latitude"] = df["latitude"].astype(float)
        df["longitude"] = df["longitude"].astype(float)
    else:
        numeric_cols = ["temperature", "humidity", "wind_speed", "precipitation", "vegetation_index", "human_activity_index", "latitude", "longitude"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df.to_dict(orient="records")  # Convert DataFrame to list of dictionaries for MongoDB

# **🔥 Upload Data to MongoDB**
def upload_to_mongo(data, collection_name):
    """Uploads processed data to MongoDB, overwriting the existing collection."""
    collection = db[collection_name]
    
    # ✅ Clear old data before inserting new
    collection.delete_many({})
    
    # ✅ Insert new data
    if data:
        collection.insert_many(data)
        return True
    return False

# **🔥 Streamlit UI**
def show():
    """Streamlit UI for file upload and testing data processing & uploading to MongoDB."""
    st.title("🚀 SAP Wildfire Management - Upload Data to MongoDB")

    uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

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
            data = process_csv(uploaded_file, is_environmental, is_current_wildfire)

            st.write("📋 **Preview Data Before Uploading**")
            st.json(data[:5])  # Show first 5 records

        if st.button("⬆️ Upload to MongoDB"):
            data = process_csv(uploaded_file, is_environmental, is_current_wildfire)
            success = upload_to_mongo(data, collection_name)

            if success:
                st.success(f"✅ Successfully uploaded to MongoDB: `{collection_name}`!")
            else:
                st.error("❌ Upload failed. No data to insert.")
