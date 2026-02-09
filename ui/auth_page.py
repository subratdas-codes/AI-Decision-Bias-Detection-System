import streamlit as st
import time

from utils.auth_manager import signup, login, admin_login
from utils.otp_manager import generate_otp, send_email_otp, send_mobile_otp
from ui.components.footer import footer


def show_auth_page():
    # 🔐 LOGIN / SIGNUP PAGE

    if "user" not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is not None:
        return

    st.markdown("""
    <div class="glass">
        <h1>🔐 Welcome to AI Decision Intelligence</h1>
        <p style="text-align:center;">
            Detect • Analyze • Correct Human Decision Bias
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ✅ OPTION DEFINED ONCE, SAFELY
    option = st.selectbox("Select Option", ["Login", "Signup"])

    # ================= SIGNUP =================
    if option == "Signup":
        username = st.text_input("Username")
        email = st.text_input("Email")
        mobile = st.text_input("Mobile Number")
        password = st.text_input("Password", type="password")

        if "otp_sent" not in st.session_state:
            st.session_state.otp_sent = False

        if not st.session_state.otp_sent:
            if st.button("Create Account"):
                if username and email and mobile and password:
                    otp = generate_otp()

                    if send_email_otp(email, otp):
                        send_mobile_otp(mobile, otp)

                        st.session_state.temp_signup = {
                            "username": username,
                            "email": email,
                            "mobile": mobile,
                            "password": password
                        }
                        st.session_state.signup_otp = otp
                        st.session_state.otp_time = time.time()
                        st.session_state.otp_sent = True

                        st.success("OTP sent to Email")
                    else:
                        st.error("Failed to send OTP")
                else:
                    st.error("Please fill all fields")

        if st.session_state.otp_sent:
            otp_input = st.text_input("Enter OTP")
            if st.button("Verify OTP"):
                if time.time() - st.session_state.otp_time > 300:
                    st.error("OTP expired")
                    st.session_state.otp_sent = False
                elif otp_input == st.session_state.signup_otp:
                    signup(**st.session_state.temp_signup)
                    st.success("Account created successfully")
                    st.session_state.otp_sent = False
                else:
                    st.error("Invalid OTP")

    # ================= LOGIN =================
    if option == "Login":
        identifier = st.text_input("Username / Email / Mobile")
        password = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login"):
                user = login(identifier, password)
                if user:
                    st.session_state.user = user
                    st.session_state.page = "Home"
                    st.rerun()
                else:
                    st.error("Invalid credentials")

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Forgot Password"):
                st.session_state.page = "forgot_password"
                st.rerun()

    footer()
    st.stop()


def admin_login_page():
    st.subheader("🔐 Admin Login")

    user_id = st.text_input("User ID")
    email = st.text_input("Email")
    mobile = st.text_input("Mobile Number")
    password = st.text_input("Password", type="password")

    if st.button("Admin Login"):
        if admin_login(user_id, email, mobile, password):
            st.session_state["admin_logged_in"] = True
            st.success("Welcome Admin 👑")
            st.rerun()
        else:
            st.error("Invalid Admin Credentials")
