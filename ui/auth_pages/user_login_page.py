import streamlit as st
from utils.auth_manager import login
from ui.styles.auth_style import auth_card_start, auth_card_end


def user_login_page():

    st.title("👤 User Login")

    identifier = st.text_input("Username / Email / Mobile")
    password = st.text_input("Password", type="password")

    col1, col2 = st.columns(2)

    # -------- LOGIN --------
    with col1:
        if st.button("Login"):

            username = login(identifier, password)

            if username:
                st.session_state.user = username
                st.session_state.role = "user"
                st.session_state.page = "Home"

                st.success("Login Successful")
                st.rerun()

            else:
                st.error("Invalid Credentials")

    # -------- FORGOT PASSWORD --------
    with col2:
        if st.button("Forgot Password"):
            st.session_state.page = "ForgotPassword"
            st.rerun()
