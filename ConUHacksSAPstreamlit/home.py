import streamlit as st

def show():
    # Page title
    st.title("🚀 SAP Wildfire Management Service")

    # Description or introduction
    st.write("Welcome to the SAP Wildfire Management Service App!")
    st.write("Navigate to **Part 1** or **Part 2** using the sidebar.")

    # File upload input
    uploaded_file = st.file_uploader("📂 Upload a CSV file", type=["csv"])

    # Dropdown for data selection
    options = [
        "Current Wildfire",
        "Historical Wildfire",
        "Historical Environmental Data",
        "Future Environmental Data"
    ]
    selected_option = st.selectbox("📊 Select Data Type", options, index=None, placeholder="Choose an option...")

    # Show submit button only if both file and option are selected
    if uploaded_file and selected_option:
        st.button("✅ Submit")
