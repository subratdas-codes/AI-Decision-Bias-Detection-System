import sys
import os

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
from utils.auth_manager import signup, login
from utils.chat_assistant import generate_chat_response
from ui.admin_dashboard import admin_dashboard



# -------- PAGE CONFIG --------
st.set_page_config(
    page_title="AI Decision Intelligence",
    page_icon="🧠",
    layout="centered"
)


# -------- SESSION --------
if "user" not in st.session_state:
    st.session_state.user = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# -------- LOGIN --------
if st.session_state.user is None:

    st.title("🔐 Login / Signup")

    option = st.selectbox("Select Option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if option == "Signup":
        if st.button("Create Account"):
            if signup(username, password):
                st.success("Account created successfully")
            else:
                st.error("Username already exists")

    if option == "Login":
        if st.button("Login"):
            if login(username, password):
                st.session_state.user = username
                st.rerun()
            else:
                st.error("Invalid credentials")

    st.stop()


# -------- SIDEBAR --------
st.sidebar.title("🧠 AI Decision System")
st.sidebar.info("Behavioral Bias Detection Tool")
st.sidebar.write(f"👤 Logged in as: {st.session_state.user}")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.rerun()

# -------- ADMIN ACCESS --------
if st.session_state.user == "admin":

    admin_dashboard()
    st.stop()



# -------- MAIN TITLE --------
st.title("🧠 AI Decision Bias Detection & Correction")
st.write("Analyze human decision patterns using AI + ML + Behavioral Intelligence")
st.divider()


# -------- INPUT --------
st.subheader("📥 Enter Decision Details")

col1, col2 = st.columns(2)

with col1:
    salary = st.number_input("💰 Expected Salary", min_value=0)

with col2:
    emotion = st.selectbox(
        "😊 Emotional State",
        ["calm", "excited", "fear", "angry"]
    )

recent_event = st.checkbox("⚡ Recent Event Influence")
ignore_options = st.checkbox("🚫 Ignored Alternative Options")

analyze = st.button("🔍 Analyze Decision", use_container_width=True)


# -------- NLP ANALYZER --------
st.divider()
st.subheader("📝 NLP Decision Text Analyzer")

decision_text = st.text_area("Describe your decision")

if st.button("Analyze Text Decision"):
    if decision_text:
        text_bias = analyze_text_decision(decision_text)
        st.success("Text Analysis Complete")
        for tb in text_bias:
            st.write("•", tb)
    else:
        st.warning("Please enter text")


# -------- RESULT --------
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

    # Save History
    record = {
        "Salary": salary,
        "Emotion": emotion,
        "Recent Event": recent_event,
        "Ignored Options": ignore_options,
        "Prediction": prediction,
        "Score": score
    }

    save_history(st.session_state.user, record)

    st.divider()

    # -------- METRIC CARDS --------
    colA, colB = st.columns(2)
    colA.metric("📊 Decision Score", f"{score}/100")
    colB.metric("🤖 ML Classification", prediction)

    st.progress(score / 100)

    st.divider()

    # -------- BIAS --------
    with st.expander("🔍 Bias Analysis Result", expanded=True):
        for b in bias_result:
            st.write("•", b)

    # -------- SUGGESTIONS --------
    with st.expander("💡 Correction Suggestions", expanded=True):
        for s in suggestions:
            st.write("•", s)

    # -------- DASHBOARD --------
    with st.expander("📊 Interactive Score Dashboard", expanded=True):

        if score >= 80:
            risk = "Low Risk / Rational Decision"
            color = "green"
        elif score >= 50:
            risk = "Moderate Risk"
            color = "orange"
        else:
            risk = "High Risk / Biased Decision"
            color = "red"

        st.markdown(f"### Risk Level: :{color}[{risk}]")

        # Gauge Chart
        gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={'text': "Decision Quality Score"},
            gauge={'axis': {'range': [0, 100]},
                   'bar': {'color': color}}
        ))

        st.plotly_chart(gauge, use_container_width=True)

        # Bar Chart
        bar = go.Figure(data=[go.Bar(
            x=["Decision Score"],
            y=[score],
            marker_color=color
        )])

        bar.update_layout(yaxis=dict(range=[0, 100]))
        st.plotly_chart(bar, use_container_width=True)

        st.info(f"Decision achieved {score}% quality rating.")

    # -------- PDF --------
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


# -------- CHAT --------
st.divider()
st.subheader("🤖 AI Chat Decision Assistant")

user_msg = st.text_input("Ask AI about your decision")

if st.button("Send Message"):
    if user_msg:
        reply = generate_chat_response(user_msg)
        st.session_state.chat_history.append(("You", user_msg))
        st.session_state.chat_history.append(("AI", reply))

for sender, msg in st.session_state.chat_history:
    if sender == "You":
        st.write(f"👤 **You:** {msg}")
    else:
        st.write(f"🤖 **AI:** {msg}")


# -------- HISTORY --------
st.divider()
st.subheader("📜 Your Decision History")

history_df = load_history(st.session_state.user)

if not history_df.empty:

    st.dataframe(history_df, use_container_width=True)

    st.subheader("🛠 Manage History")

    record_id = st.number_input("Enter Record ID to Delete", min_value=0)

    if st.button("Delete Selected Record"):
        delete_record(record_id)
        st.success("Record Deleted")
        st.rerun()

    if st.button("Clear All History"):
        delete_all(st.session_state.user)
        st.success("All History Deleted")
        st.rerun()

else:
    st.write("No history available yet.")
