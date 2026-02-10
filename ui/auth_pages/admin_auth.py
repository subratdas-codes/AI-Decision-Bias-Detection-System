import streamlit as st

# ================================
# ADMIN CREDENTIALS
# ================================
ADMIN_USERNAME = "Admin"
ADMIN_EMAIL = "byteconnect360@gmail.com"
ADMIN_MOBILE = "9090535566"
ADMIN_PASSWORD = "admin123"


def admin_login_page():

    st.title("🛠 Admin Login")

    identifier = st.text_input("Admin ID / Email / Mobile")
    password = st.text_input("Password", type="password")

    if st.button("Admin Login"):

        if (
            identifier in [ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_MOBILE]
            and password == ADMIN_PASSWORD
        ):
            # ✅ SET STANDARD SESSION KEYS
            st.session_state.is_admin = True
            st.session_state.is_user = False
            st.session_state.username = "Admin"
            st.session_state.page = "admin_dashboard"

            st.success("Admin Login Successful ✅")
            st.rerun()

        else:
            st.error("Invalid Admin Credentials ❌")
