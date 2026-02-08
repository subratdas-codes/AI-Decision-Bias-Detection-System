import streamlit as st
from utils.auth_manager import (
    update_email,
    update_mobile,
    change_password
)
from utils.otp_manager import generate_otp, send_email_otp



def profile_menu(username):

    with st.expander(f"👤 {username}", expanded=False):

        menu = st.radio(
            "Profile Menu",
            ["Edit Profile", "Change Password", "Logout"]
        )

        # =====================================
        # EDIT PROFILE
        # =====================================
        if menu == "Edit Profile":

            option = st.radio(
                "Choose Update Option",
                ["Edit Email", "Edit Mobile"]
            )

            # -------- EDIT EMAIL --------
            if option == "Edit Email":

                new_email = st.text_input("Enter New Email")

                if "email_otp_sent" not in st.session_state:
                    st.session_state.email_otp_sent = False

                if "email_otp" not in st.session_state:
                    st.session_state.email_otp = None

                if not st.session_state.email_otp_sent:

                    if st.button("Send OTP"):

                        otp = generate_otp()

                        if send_email_otp(new_email, otp):
                            st.session_state.email_otp = otp
                            st.session_state.email_otp_sent = True
                            st.success("OTP Sent")
                        else:
                            st.error("OTP Send Failed")

                else:

                    entered_otp = st.text_input("Enter OTP")

                    if st.button("Verify & Update"):

                        if entered_otp == st.session_state.email_otp:

                            if update_email(username, new_email):
                                st.success("Email Updated")

                                st.session_state.email_otp_sent = False
                                st.session_state.email_otp = None
                            else:
                                st.error("Email Already Exists")

                        else:
                            st.error("Invalid OTP")

            # -------- EDIT MOBILE --------
            elif option == "Edit Mobile":

                new_mobile = st.text_input("Enter New Mobile")

                if st.button("Update Mobile"):
                    if update_mobile(username, new_mobile):
                        st.success("Mobile Updated")
                    else:
                        st.error("Mobile Already Exists")

        # =====================================
        # CHANGE PASSWORD
        # =====================================
        elif menu == "Change Password":

            old_pass = st.text_input("Current Password", type="password")
            new_pass = st.text_input("New Password", type="password")
            confirm_pass = st.text_input("Confirm Password", type="password")

            if st.button("Change Password"):

                if new_pass != confirm_pass:
                    st.error("Passwords do not match")

                elif change_password(username, old_pass, new_pass):
                    st.success("Password Changed")

                else:
                    st.error("Wrong Current Password")

        # =====================================
        # LOGOUT
        # =====================================
        elif menu == "Logout":

            if st.button("Confirm Logout"):

                st.session_state.user = None
                st.session_state.role = None
                st.session_state.page = "Home"

                st.success("Logged out successfully")
                st.rerun()
