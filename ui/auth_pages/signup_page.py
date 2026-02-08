import streamlit as st
import time

from utils.auth_manager import signup, user_exists
from utils.otp_manager import generate_otp, send_email_otp


def signup_page():

    st.title("User Signup")

    username = st.text_input("Username")
    email = st.text_input("Email")
    mobile = st.text_input("Mobile Number")
    password = st.text_input("Password", type="password")

    # -------- SEND OTP --------
    if st.button("Send OTP"):

        if not username or not email or not mobile or not password:
            st.error("All fields are mandatory")
            return

        if user_exists(username=username):
            st.error("Username already exists")
            return

        if user_exists(email=email):
            st.error("Email already exists")
            return

        if user_exists(mobile=mobile):
            st.error("Mobile already exists")
            return

        otp = generate_otp()

        st.session_state.signup_otp = otp
        st.session_state.otp_time = time.time()

        st.session_state.signup_data = {
            "username": username,
            "email": email,
            "mobile": mobile,
            "password": password
        }

        if send_email_otp(email, otp):
            st.success("OTP sent to email")
            st.session_state.otp_sent = True
        else:
            st.error("OTP sending failed")

    # -------- VERIFY OTP --------
    if st.session_state.get("otp_sent"):

        user_otp = st.text_input("Enter OTP")

        if st.button("Verify & Signup"):

            # OTP Expiry (5 min)
            if time.time() - st.session_state.otp_time > 300:
                st.error("OTP expired")
                return

            if user_otp == st.session_state.signup_otp:

                data = st.session_state.signup_data

                if signup(
                    data["username"],
                    data["email"],
                    data["mobile"],
                    data["password"]
                ):

                    st.success("Signup Successful")

                    # Clear session
                    st.session_state.otp_sent = False
                    st.session_state.pop("signup_otp", None)
                    st.session_state.pop("signup_data", None)
                    st.session_state.pop("otp_time", None)

                else:
                    st.error("User already exists")

            else:
                st.error("Invalid OTP")
