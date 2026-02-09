import streamlit as st

from rule_engine.bias_rules import detect_bias
from ml_model.decision_scoring import calculate_decision_score
from utils.correction_engine import suggest_corrections


def show_career_service():

    st.markdown("## 🎓 Career Decision Support")
    st.write(
        "Analyze career-related decisions using AI-powered bias detection."
    )

    st.divider()

    # -------- INPUTS --------
    career_options = st.text_area(
        "Career Options You Are Considering",
        placeholder="Example: Software Engineer, Data Analyst, MBA..."
    )

    experience_years = st.slider(
        "Your Experience (Years)",
        0, 30, 1
    )

    confidence_level = st.selectbox(
        "Confidence Level",
        ["low", "medium", "high"]
    )

    emotion = st.selectbox(
        "Current Emotional State",
        ["calm", "excited", "fear", "confused"]
    )

    social_pressure = st.checkbox(
        "Feeling pressure from family / society?"
    )

    st.divider()

    analyze = st.button("🔍 Analyze Career Decision")

    # -------- ANALYSIS --------
    if analyze:
        decision_data = {
            "career_options": career_options,
            "experience": experience_years,
            "confidence_level": confidence_level,
            "emotion": emotion,
            "social_pressure": social_pressure
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
