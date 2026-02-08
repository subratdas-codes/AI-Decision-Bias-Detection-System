import streamlit as st
from utils.auth_manager import (
    update_email,
    update_mobile,
    change_password
)


def profile_dropdown(username):

    with st.expander(f"👤 {username}", expanded=False):

        option = st.selectbox(
            "Profile Options",
            [
                "Edit Email",
                "Edit Mobile",
                "Change Password",
                "Logout"
            ]
        )

        # -------- EDIT EMAIL --------
        if option == "Edit Email":

            new_email = st.text_input("Enter New Email")

            if st.button("Update Email"):
                if update_email(username, new_email):
                    st.success("Email Updated")
                else:
                    st.error("Email already exists")

        # -------- EDIT MOBILE --------
        elif option == "Edit Mobile":

            new_mobile = st.text_input("Enter New Mobile")

            if st.button("Update Mobile"):
                if update_mobile(username, new_mobile):
                    st.success("Mobile Updated")
                else:
                    st.error("Mobile already exists")

        # -------- CHANGE PASSWORD --------
        elif option == "Change Password":

            old_pass = st.text_input("Old Password", type="password")
            new_pass = st.text_input("New Password", type="password")

            if st.button("Change Password"):
                if change_password(username, old_pass, new_pass):
                    st.success("Password Changed")
                else:
                    st.error("Wrong Old Password")

        # -------- LOGOUT --------
        elif option == "Logout":

            if st.button("Confirm Logout"):
                st.session_state.user = None
                st.session_state.role = None
                st.session_state.page = "Home"
                st.rerun()
