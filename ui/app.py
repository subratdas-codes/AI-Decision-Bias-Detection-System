import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st

# -------- PAGE IMPORTS --------
from ui.custom_pages.home_page import home_page
from ui.custom_pages.about_page import about_page
from ui.custom_pages.services_page import services_page

from ui.admin_dashboard import admin_dashboard
from ui.profile_page import profile_page

# ⭐ AUTH PAGES
from ui.auth_pages.user_login_page import user_login_page
from ui.auth_pages.admin_login_page import admin_login_page
from ui.auth_pages.signup_page import signup_page
from ui.auth_pages.forgot_password_page import forgot_password_page

# -------- COMPONENTS --------
from ui.components.navbar import navbar
from ui.components.footer import footer

# -------- STYLE IMPORTS --------
from ui.styles.global_style import load_global_style
from ui.styles.auth_style import load_auth_style

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="AI Decision Intelligence",
    page_icon="🧠",
    layout="wide"
)


# =====================================
# LOAD FRONTEND STYLES
# =====================================
load_global_style()
load_auth_style()


# =====================================
# SESSION STATE
# =====================================
if "user" not in st.session_state:
    st.session_state.user = None

if "role" not in st.session_state:
    st.session_state.role = None

if "page" not in st.session_state:
    st.session_state.page = "Home"
    
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False



# =====================================
# NAVBAR (ALWAYS VISIBLE)
# =====================================
navbar()

# =====================================
# ADMIN DIRECT DASHBOARD
# =====================================
if st.session_state.role == "admin":
    admin_dashboard()
    footer()
    st.stop()


# =====================================
# PAGE ROUTING
# =====================================

# -------- HOME --------
if st.session_state.page == "Home":
    home_page()


# -------- ABOUT --------
elif st.session_state.page == "About":
    about_page()


# -------- SERVICES --------
elif st.session_state.page == "Services":

    if st.session_state.user:
        services_page(st.session_state.user)
    else:
        st.warning("🔐 Login required to access services")


# -------- PROFILE / AUTH --------
elif st.session_state.page == "Profile":

    # USER LOGGED IN
    if st.session_state.user:
        profile_page(st.session_state.user)

    # PUBLIC LOGIN / SIGNUP
    else:

        option = st.radio(
            "Choose Option",
            ["Login", "Signup"]
        )

        # LOGIN FLOW
        if option == "Login":

            login_type = st.radio(
                "Login Type",
                ["User Login", "Admin Login"]
            )

            if login_type == "User Login":
                user_login_page()

            elif login_type == "Admin Login":
                admin_login_page()

        # SIGNUP FLOW
        elif option == "Signup":
            signup_page()



# -------- FORGOT PASSWORD --------
elif st.session_state.page == "ForgotPassword":

    forgot_password_page()

    if st.button("⬅ Back to Login", key="back_login"):
        st.session_state.page = "Profile"
        st.rerun()


# =====================================
# FOOTER
# =====================================
footer()
