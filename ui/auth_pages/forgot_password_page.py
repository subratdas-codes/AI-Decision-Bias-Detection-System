import streamlit as st

from utils.otp_manager import generate_otp, send_email_otp
from utils.auth_manager import (
    get_username_by_email,
    reset_password_by_email
)


def forgot_password_page():

    st.title("🔐 Forgot Password")

    email = st.text_input("Enter Registered Email")

    # -------- SESSION STATE --------
    if "otp_sent" not in st.session_state:
        st.session_state.otp_sent = False

    if "generated_otp" not in st.session_state:
        st.session_state.generated_otp = None


    # =====================================
    # SEND OTP
    # =====================================
    if not st.session_state.otp_sent:

        if st.button("Send OTP"):

            username = get_username_by_email(email)

            if username:

                otp = generate_otp()

                if send_email_otp(email, otp):
                    st.session_state.generated_otp = otp
                    st.session_state.otp_sent = True
                    st.success("OTP Sent Successfully")

                else:
                    st.error("Failed to send OTP")

            else:
                st.error("Email not registered")


    # =====================================
    # OTP VERIFICATION
    # =====================================
    if st.session_state.otp_sent:

        entered_otp = st.text_input("Enter OTP")
        new_password = st.text_input("New Password", type="password")

        col1, col2 = st.columns(2)

        # -------- RESET PASSWORD --------
        with col1:
            if st.button("Reset Password"):

                if entered_otp == st.session_state.generated_otp:

                    if reset_password_by_email(email, new_password):

                        st.success("Password Reset Successful")

                        # RESET SESSION
                        st.session_state.otp_sent = False
                        st.session_state.generated_otp = None

                    else:
                        st.error("Password Reset Failed")

                else:
                    st.error("Invalid OTP")

        # -------- BACK BUTTON --------
