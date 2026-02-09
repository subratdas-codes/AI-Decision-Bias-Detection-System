import streamlit as st
from utils.auth_manager import login


def user_login_page():

    st.markdown("## 👤 User Login")

    identifier = st.text_input("Username / Email / Mobile")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns([1, 1])

    # -------- LOGIN --------
    with col1:
        if st.button("Login"):
            username = login(identifier, password)

            if username:
                st.session_state.user = username
                st.session_state.page = "Service"
                st.success("Login Successful")
                st.rerun()
            else:
                st.error("Invalid Credentials")

    # -------- FORGOT PASSWORD --------
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Forgot Password"):
            st.session_state.page = "forgot_password"
            st.rerun()
from ui.components.footer import footer
footer()
