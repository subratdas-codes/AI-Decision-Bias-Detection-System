import streamlit as st
from ui.custom_pages.dashboard_page import dashboard_page


def services_page(username):

    st.title("🧩 Decision Analysis Services")

    category = st.selectbox(
        "Select Decision Category",
        [
            "Career Decision",
            "HR Hiring Decision",
            "Salary Decision",
            "Social Decision",
            "Custom Decision"
        ]
    )

    st.success(f"Selected: {category}")

    st.divider()

    dashboard_page(username)
