import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import plotly.graph_objects as go

from rule_engine.bias_rules import detect_bias
from utils.correction_engine import suggest_corrections
from ml_model.decision_scoring import calculate_decision_score
from ml_model.predict_model import predict_decision
from utils.history_manager import load_history
from utils.report_generator import generate_pdf
from utils.nlp_analyzer import analyze_text_decision
from utils.chat_assistant import generate_chat_response

from ui.navbar import show_navbar
from ui.home_page import show_home_page
from ui.auth_page import show_auth_page


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Decision Intelligence",
    page_icon="🧠",
    layout="centered"
)

# ---------------- GLOBAL CSS ----------------
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
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}

h1, h2, h3 { color: #e5f2f7 !important; }
label, h4 { color: #d1e7ee !important; }
p, span, div, small { color: #c7dfe6 !important; }

input, textarea, select {
    background: rgba(255,255,255,0.95) !important;
    color: black !important;
    border-radius: 12px !important;
    font-weight: 600;
}

button {
    background: linear-gradient(135deg, #00c6ff, #0072ff) !important;
    color: white !important;
    border-radius: 14px !important;
    height: 45px;
    font-weight: bold;
    border: none;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "page" not in st.session_state:
    st.session_state.page = "Home"


# =====================================================
# NAVBAR (VISIBLE EVERYWHERE)
# =====================================================
show_navbar()
st.divider()


# =====================================================
# PAGE ROUTING
# =====================================================

# 🏠 HOME (PUBLIC)
if st.session_state.page == "Home":
    show_home_page()
    st.stop()

# 👤 PROFILE (LOGIN PAGE)
if st.session_state.page == "Profile":
    if st.session_state.user is None:
        show_auth_page()
        st.stop()

# 🛠 SERVICE (PUBLIC)
if st.session_state.page == "Service":
    st.markdown("## 🛠 Services")
    st.write("AI-powered decision bias detection, scoring and recommendations.")
    st.stop()


# =====================================================
# DASHBOARD (ONLY AFTER LOGIN)
# =====================================================
if st.session_state.user is None:
    st.stop()


# =====================================================
# MAIN DASHBOARD
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
