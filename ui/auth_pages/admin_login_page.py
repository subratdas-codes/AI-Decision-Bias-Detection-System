import streamlit as st

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

            st.session_state.user = "admin"
            st.session_state.role = "admin"
            st.session_state.page = "Home"

            st.success("Admin Login Successful")
            st.rerun()

        else:
            st.error("Invalid Admin Credentials")
