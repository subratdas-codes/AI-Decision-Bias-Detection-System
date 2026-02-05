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
from utils.history_manager import save_history, load_history, delete_record, delete_all
from utils.report_generator import generate_pdf
from utils.nlp_analyzer import analyze_text_decision
from utils.auth_manager import signup, login, change_password, delete_user_account
from utils.chat_assistant import generate_chat_response
from ui.admin_dashboard import admin_dashboard
from ui.profile_page import profile_page
from utils.otp_manager import generate_otp, send_email_otp, send_mobile_otp

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Decision Intelligence",
    page_icon="🧠",
    layout="centered"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
<style>

/* REMOVE STREAMLIT DEFAULT UI */
header[data-testid="stHeader"] {display: none;}
div[data-testid="stToolbar"] {display: none;}
footer {visibility: hidden;}

/* BACKGROUND */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    font-family: 'Segoe UI', sans-serif;
}

/* CENTER CONTAINER */
.block-container {
    padding-top: 2rem;
    max-width: 800px;
}

/* GLASS CARD */
.glass {
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(16px);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}

/* TEXT */
h1, h2, h3, label, p, span {
    color: white !important;
}

/* INPUTS */
input, textarea, select {
    background: rgba(255,255,255,0.95) !important;
    color: black !important;
    border-radius: 12px !important;
    font-weight: 600;
}

/* FIX NUMBER INPUT VISIBILITY */
input[type="number"] {
    color: black !important;
    font-weight: 700 !important;
}

input[type="number"]::placeholder {
    color: #444 !important;
}

/* FIX +/- BUTTON */
button[kind="secondary"] {
    color: black !important;
}

/* BUTTONS */
button {
    background: linear-gradient(135deg, #00c6ff, #0072ff) !important;
    color: white !important;
    border-radius: 14px !important;
    height: 45px;
    font-weight: bold;
    border: none;
}

button:hover {
    transform: scale(1.03);
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #141e30, #243b55);
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# =====================================================
# 🔐 LOGIN / SIGNUP SECTION
# =====================================================
if st.session_state.user is None:

    st.markdown("""
    <div class="glass">
        <h1>🔐 Welcome to AI Decision Intelligence</h1>
        <p style="text-align:center; font-size:18px;">
            Detect • Analyze • Correct Human Decision Bias
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    option = st.selectbox("Select Option", ["Login", "Signup"])

    # ================= SIGNUP =================
    if option == "Signup":

        username = st.text_input("Username")
        email = st.text_input("Email")
        mobile = st.text_input("Mobile Number")
        password = st.text_input("Password", type="password")

        if "otp_sent" not in st.session_state:
            st.session_state.otp_sent = False

        # -------- SEND OTP --------
        if not st.session_state.otp_sent:

            if st.button("Create Account"):

                if username and email and mobile and password:

                    otp = generate_otp()

                    email_status = send_email_otp(email, otp)
                    send_mobile_otp(mobile, otp)  # simulation

                    if email_status:

                        st.session_state.temp_signup = {
                            "username": username,
                            "email": email,
                            "mobile": mobile,
                            "password": password
                        }

                        st.session_state.signup_otp = otp
                        st.session_state.otp_time = time.time()
                        st.session_state.otp_sent = True

                        st.success("OTP sent to Email (Mobile OTP simulated)")

                    else:
                        st.error("Failed to send Email OTP")

                else:
                    st.error("Fill all fields")


        # -------- VERIFY OTP --------
        if st.session_state.otp_sent:

            otp_input = st.text_input("Enter OTP")

            if st.button("Verify OTP"):

                # OTP expiry → 5 minutes
                if time.time() - st.session_state.otp_time > 300:
                    st.error("OTP expired")
                    st.session_state.otp_sent = False

                elif otp_input == st.session_state.signup_otp:

                    data = st.session_state.temp_signup

                    if signup(
                        data["username"],
                        data["email"],
                        data["mobile"],
                        data["password"]
                    ):
                        st.success("Account Created Successfully")
                        st.session_state.otp_sent = False

                    else:
                        st.error("User already exists")

                else:
                    st.error("Invalid OTP")


    # ================= LOGIN =================
    if option == "Login":

        identifier = st.text_input("Username / Email / Mobile")
        password = st.text_input("Password", type="password")

        if st.button("Login"):

            user = login(identifier, password)

            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Invalid Credentials")

    st.stop()



# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.title("🧠 AI Decision System")
st.sidebar.info("Behavioral Bias Detection Tool")
st.sidebar.write(f"👤 Logged in as: {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

page = st.sidebar.radio("Navigation", ["Dashboard", "Profile"])

if page == "Profile":
    profile_page(st.session_state.user)
    st.stop()





# -------- DELETE ACCOUNT --------
if st.sidebar.button("🗑 Delete My Account"):

    delete_user_account(st.session_state.user)
    st.session_state.user = None
    st.rerun()


# -------- ADMIN ACCESS --------
if st.session_state.user == "admin":
    admin_dashboard()
    st.stop()


# =====================================================
# MAIN DASHBOARD
# =====================================================
st.title("🧠 AI Decision Bias Detection & Correction")
st.write("Analyze decision patterns using AI + ML + Behavioral Science")
st.divider()


# ---------------- INPUT ----------------
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
        text_bias = analyze_text_decision(decision_text)
        for tb in text_bias:
            st.write("•", tb)
    else:
        st.warning("Please enter text")


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

    record = {
        "Salary": salary,
        "Emotion": emotion,
        "Prediction": prediction,
        "Score": score
    }

    colA, colB = st.columns(2)
    colA.metric("📊 Decision Score", f"{score}/100")
    colB.metric("🤖 ML Classification", prediction)

    st.progress(score / 100)


    with st.expander("🔍 Bias Analysis Result", expanded=True):
        for b in bias_result:
            st.write("•", b)

    with st.expander("💡 Correction Suggestions", expanded=True):
        for s in suggestions:
            st.write("•", s)


    # -------- GAUGE CHART --------
    if score >= 80:
        risk = "Low Risk"
        color = "green"
    elif score >= 50:
        risk = "Moderate Risk"
        color = "orange"
    else:
        risk = "High Risk"
        color = "red"

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Decision Quality Score"},
        gauge={'axis': {'range': [0, 100]},
               'bar': {'color': color}}
    ))

    st.plotly_chart(gauge, use_container_width=True)

    pdf_file = generate_pdf(
        decision_data,
        bias_result,
        suggestions,
        score,
        prediction,
        risk
    )

    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download Decision Report", f)


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

    record_id = st.number_input("Enter Record ID to Delete", min_value=0)

    if st.button("Delete Selected Record"):
        delete_record(record_id)
        st.rerun()

    if st.button("Clear All History"):
        delete_all(st.session_state.user)
        st.rerun()

if not history.empty:
    st.dataframe(history, use_container_width=True)
else:
    st.info("No history yet")
