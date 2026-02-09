import streamlit as st

from rule_engine.bias_rules import detect_bias
from ml_model.decision_scoring import calculate_decision_score
from utils.correction_engine import suggest_corrections


def show_hr_service():

    st.markdown("## 🧑‍💼 HR Hiring Bias Detection")
    st.write(
        "Analyze hiring decisions to detect unconscious bias and improve fairness."
    )

    st.divider()

    # -------- INPUTS --------
    role = st.text_input(
        "Role Being Hired For",
        placeholder="Example: Software Engineer"
    )

    candidate_background = st.text_area(
        "Candidate Background Summary",
        placeholder="Education, experience, skills..."
    )

    similarity_bias = st.checkbox(
        "Candidate feels similar to me (same college, background, culture)"
    )

    first_impression = st.selectbox(
        "First Impression of Candidate",
        ["positive", "neutral", "negative"]
    )

    emotion = st.selectbox(
        "Current Emotional State",
        ["calm", "stressed", "tired", "excited"]
    )

    st.divider()

    analyze = st.button("🔍 Analyze Hiring Decision")

    # -------- ANALYSIS --------
    if analyze:
        decision_data = {
            "role": role,
            "candidate_background": candidate_background,
            "similarity_bias": similarity_bias,
            "first_impression": first_impression,
            "emotion": emotion
        }

        bias_result = detect_bias(decision_data)
        score = calculate_decision_score(bias_result)
        suggestions = suggest_corrections(bias_result)

        st.subheader("📊 Analysis Result")
        st.metric("Decision Fairness Score", f"{score}/100")

        st.progress(score / 100)

        st.subheader("⚠ Detected Biases")
        for b in bias_result:
            st.write("•", b)

        st.subheader("💡 Recommendations")
        for s in suggestions:
            st.write("•", s)

        st.divider()

        if st.button("⬅ Back to Services"):
            st.session_state.page = "Service"
            st.rerun()
