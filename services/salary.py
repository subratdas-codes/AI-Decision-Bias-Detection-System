import streamlit as st

from rule_engine.bias_rules import detect_bias
from ml_model.decision_scoring import calculate_decision_score
from utils.correction_engine import suggest_corrections


def show_salary_page():


    st.markdown("## 💰 Salary Decision Analysis")
    st.write(
        "Analyze whether your salary decision is driven by logic or influenced by bias."
    )

    st.divider()

    # -------- INPUTS --------
    current_salary = st.number_input(
        "Current Salary", min_value=0, step=1000
    )

    offered_salary = st.number_input(
        "Offered Salary", min_value=0, step=1000
    )

    experience = st.slider(
        "Years of Experience", 0, 30, 2
    )

    emotion = st.selectbox(
        "Current Emotional State",
        ["calm", "excited", "fear", "anxious"]
    )

    risk_tolerance = st.selectbox(
        "Risk Tolerance",
        ["low", "medium", "high"]
    )

    external_pressure = st.checkbox(
        "Feeling pressure from family / friends?"
    )

    st.divider()

    analyze = st.button("🔍 Analyze Salary Decision")

    # -------- ANALYSIS --------
    if analyze:
        decision_data = {
            "current_salary": current_salary,
            "offered_salary": offered_salary,
            "experience": experience,
            "emotion": emotion,
            "risk_tolerance": risk_tolerance,
            "external_pressure": external_pressure
        }

        bias_result = detect_bias(decision_data)
        score = calculate_decision_score(bias_result)
        suggestions = suggest_corrections(bias_result)

        st.subheader("📊 Analysis Result")
        st.metric("Decision Score", f"{score}/100")

        st.progress(score / 100)

        st.subheader("⚠ Detected Biases")
        for b in bias_result:
            st.write("•", b)

        st.subheader("💡 Suggestions")
        for s in suggestions:
            st.write("•", s)

        st.divider()

        if st.button("⬅ Back to Services"):
            st.session_state.page = "Service"
            st.rerun()
