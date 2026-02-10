import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.graph_objects as go

# =====================================
# ⭐ SESSION INITIALIZATION
# =====================================
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =====================================
# 🔁 SESSION COMPATIBILITY BRIDGE (ADDED)
# =====================================
# This bridges your OLD system with NEW admin panel
if "is_admin" not in st.session_state:
    st.session_state.is_admin = st.session_state.admin_logged_in

if "is_user" not in st.session_state:
    st.session_state.is_user = st.session_state.user is not None

if "username" not in st.session_state:
    st.session_state.username = st.session_state.user


# =====================================
# IMPORTS
# =====================================
from rule_engine.bias_rules import detect_bias
from utils.correction_engine import suggest_corrections
from ml_model.decision_scoring import calculate_decision_score
from ml_model.predict_model import predict_decision
from utils.history_manager import load_history
from utils.nlp_analyzer import analyze_text_decision
from utils.chat_assistant import generate_chat_response

from ui.navbar import show_navbar
from ui.home_page import show_home_page
from ui.auth_page import show_auth_page, admin_login_page
from ui.admin_dashboard import admin_dashboard
from ui.service_page import show_service_page
from services.salary import show_salary_page
from services.career import show_career_service
from services.hr import show_hr_service
from services.social import show_social_service
from services.policy import show_policy_service
from ui.auth_pages.forgot_password_page import forgot_password_page

from ui.components.footer import footer


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Decision Intelligence",
    page_icon="🧠",
    layout="centered"
)

# =====================================================
# GLOBAL CSS
# =====================================================
st.markdown("""
<style>
header[data-testid="stHeader"] {display:none;}
div[data-testid="stToolbar"] {display:none;}
footer {visibility:hidden;}

.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    font-family: 'Segoe UI', sans-serif;
}

.block-container {
    padding-top: 2rem;
    max-width: 900px;
}

.glass {
    background: rgba(255,255,255,0.18);
    backdrop-filter: blur(16px);
    border-radius: 22px;
    padding: 22px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.35);
}

h1, h2, h3, h4 {
    color: #f1fbff !important;
    font-weight: 600;
}

p, span, small {
    color: #d9edf3 !important;
}

label {
    color: #e6f6fb !important;
    font-weight: 500;
}

input, textarea, select {
    background-color: #f8fafc !important;
    color: #0f172a !important;
    border-radius: 12px !important;
    font-weight: 500;
}

input::placeholder,
textarea::placeholder {
    color: #64748b !important;
}

button {
    background: linear-gradient(135deg, #4fd1c5, #38b2ac) !important;
    color: #0b1f24 !important;
    border-radius: 14px !important;
    height: 44px;
    font-weight: 600;
    border: none;
}

.nav-logo {
    font-size: 18px;
    font-weight: 800;
    color: #eafffb !important;
    letter-spacing: 0.4px;
}

.nav-btn button {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    font-size: 15px;
    font-weight: 600;
    color: #eafffb !important;
    padding: 6px 16px;
    border-radius: 18px;
}

.nav-btn button:hover {
    color: #9fb4bd !important;
}

.nav-active button {
    background: rgba(79, 209, 197, 0.35) !important;
    color: #ffffff !important;
}

.service-card {
    padding: 22px;
    min-height: 190px;
    margin-bottom: 12px;
    background: rgba(255,255,255,0.18);
    border-radius: 22px;
}
</style>
""", unsafe_allow_html=True)



# =====================================================
# NAVBAR (VISIBLE EVERYWHERE)
# =====================================================
show_navbar()
st.divider()


# =====================================================
# 🔐 FORGOT PASSWORD ROUTE
# =====================================================
if st.session_state.page == "forgot_password":
    forgot_password_page()
    footer()
    st.stop()


# =====================================================
# PAGE ROUTING
# =====================================================

# ---- ADMIN ----
if st.session_state.page == "Admin":
    if st.session_state.admin_logged_in:
        admin_dashboard()
    else:
        admin_login_page()
    footer()
    st.stop()

# ---- ABOUT ----
if st.session_state.page == "About":
    st.markdown("## ℹ️ About Project Human Bias (PHB)")
    st.write(
        "PHB analyzes human decision-making, detects cognitive & emotional biases, "
        "and provides AI-driven guidance for better choices."
    )
    footer()
    st.stop()

# ---- HOME ----
if st.session_state.page == "Home":
    show_home_page()
    footer()
    st.stop()

# ---- PROFILE (LOGIN / SIGNUP) ----
if st.session_state.page == "Profile":
    if st.session_state.user is None:
        show_auth_page()
    else:
        st.session_state.page = "Service"
        st.rerun()
    footer()
    st.stop()

# ---- SERVICE ----
if st.session_state.page == "Service":
    if st.session_state.user is None:
        st.session_state.page = "Profile"
        st.rerun()
    else:
        show_service_page()
    footer()
    st.stop()

# ---- SALARY ----
if st.session_state.page == "salary":
    if st.session_state.user is None:
        st.session_state.page = "Profile"
        st.rerun()
    else:
        show_salary_page()
    footer()
    st.stop()

# ---- CAREER ----
if st.session_state.page == "career":
    if st.session_state.user is None:
        st.session_state.page = "Profile"
        st.rerun()
    else:
        show_career_service()
    footer()
    st.stop()

# ---- HR ----
if st.session_state.page == "hr":
    if st.session_state.user is None:
        st.session_state.page = "Profile"
        st.rerun()
    else:
        show_hr_service()
    footer()
    st.stop()

# ---- SOCIAL ----
if st.session_state.page == "social":
    if st.session_state.user is None:
        st.session_state.page = "Profile"
        st.rerun()
    else:
        show_social_service()
    footer()
    st.stop()

# ---- POLICY ----
if st.session_state.page == "policy":
    if st.session_state.user is None:
        st.session_state.page = "Profile"
        st.rerun()
    else:
        show_policy_service()
    footer()
    st.stop()


# =====================================================
# USER DASHBOARD (ONLY FOR LOGGED-IN USERS)
# =====================================================
if st.session_state.user is None:
    st.stop()


# =====================================================
# MAIN USER DASHBOARD
# =====================================================
st.title("🧠 AI Decision Bias Detection & Correction")
st.write("Analyze decision patterns using AI + ML + Behavioral Science")
st.divider()

st.subheader("📥 Decision Inputs")

col1, col2 = st.columns(2)

with col1:
    salary = st.number_input("💰 Expected Salary", min_value=0, value=50000)

with col2:
    emotion = st.selectbox("😊 Emotional State", ["calm", "excited", "fear", "angry"])

recent_event = st.checkbox("⚡ Recent Event Influence")
ignore_options = st.checkbox("🚫 Ignored Alternative Options")

analyze = st.button("🔍 Analyze Decision", use_container_width=True)


# =====================================================
# NLP ANALYZER
# =====================================================
st.divider()
st.subheader("📝 NLP Text Analyzer")

decision_text = st.text_area("Describe your decision")

if st.button("Analyze Text"):
    if decision_text:
        for tb in analyze_text_decision(decision_text):
            st.write("•", tb)


# =====================================================
# RESULT
# =====================================================
if analyze:
    decision_data = {
        "expected_salary": salary,
        "recent_event_impact": recent_event,
        "emotional_state": emotion,
        "ignored_alternative_options": ignore_options
    }

    bias_result = detect_bias(decision_data)
    suggestions = suggest_corrections(bias_result)
    score = calculate_decision_score(bias_result)
    prediction = predict_decision(decision_data)

    colA, colB = st.columns(2)
    colA.metric("📊 Decision Score", f"{score}/100")
    colB.metric("🤖 ML Classification", prediction)

    st.progress(score / 100)


# =====================================================
# CHAT ASSISTANT
# =====================================================
st.divider()
st.subheader("🤖 AI Decision Assistant")

msg = st.text_input("Ask AI about your decision")

if st.button("Send"):
    reply = generate_chat_response(msg)
    st.session_state.chat_history.append(("You", msg))
    st.session_state.chat_history.append(("AI", reply))

for sender, text in st.session_state.chat_history:
    st.write(f"**{sender}:** {text}")


# =====================================================
# HISTORY
# =====================================================
st.divider()
st.subheader("📜 Decision History")

history_df = load_history(st.session_state.user)

if not history_df.empty:
    st.dataframe(history_df, use_container_width=True)
else:
    st.info("No history yet")


# =====================================================
# CUSTOM FOOTER (NOT STREAMLIT FOOTER)
# =====================================================
footer()
