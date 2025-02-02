# Import streamlit first
import streamlit as st

# Set Streamlit page to wide layout (Full screen map) - this must be first
st.set_page_config(page_title="SAP Wildfire Management", layout="wide")

import home
import part1
import part2

# Initialize session state for page navigation
if "page" not in st.session_state:
    st.session_state.page = "Home"

# Sidebar navigation (Vertical Navigation Bar)
page = st.sidebar.selectbox("Choose a Page", ["Home", "Part 1", "Part 2"])

# Update session state with the selected page
st.session_state.page = page

# Show the content based on the selected page
if st.session_state.page == "Home":
    home.show()
elif st.session_state.page == "Part 1":
    part1.show()
elif st.session_state.page == "Part 2":
    part2.show()
