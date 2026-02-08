import streamlit as st
import plotly.graph_objects as go

from rule_engine.bias_rules import detect_bias
from utils.correction_engine import suggest_corrections
from ml_model.decision_scoring import calculate_decision_score
from ml_model.predict_model import predict_decision
from utils.history_manager import save_history
from utils.report_generator import generate_pdf
from utils.nlp_analyzer import analyze_text_decision


def dashboard_page(username):

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

    # NLP
    st.divider()
    st.subheader("📝 NLP Decision Text Analyzer")

    decision_text = st.text_area("Describe your decision")

    if st.button("Analyze Text Decision"):
        if decision_text:
            text_bias = analyze_text_decision(decision_text)
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

        record = {
            "Salary": salary,
            "Emotion": emotion,
            "Recent Event": recent_event,
            "Ignored Options": ignore_options,
            "Prediction": prediction,
            "Score": score
        }

        save_history(username, record)

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

        # Gauge
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
