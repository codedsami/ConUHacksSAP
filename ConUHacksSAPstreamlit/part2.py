import streamlit as st

def show():
    st.title("🌿 Part 2: Environmental Analysis")

    # Content for Part 2
    age = st.number_input("Enter your age:", min_value=1, max_value=100, key="age_part2")
    if st.button("Submit Age", key="submit_age_part2"):
        st.info(f"Your age is {age}. This is Part 2.")
