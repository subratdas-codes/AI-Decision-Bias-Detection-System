import streamlit as st

from rule_engine.bias_rules import detect_bias
from ml_model.decision_scoring import calculate_decision_score
from utils.correction_engine import suggest_corrections


def show_social_service():

    st.markdown("## 🌍 Social Decision Analysis")
    st.write(
        "Analyze how social influence and emotions affect your decisions."
    )

    st.divider()

    # -------- INPUTS --------
    decision_context = st.text_area(
        "Describe the Decision",
        placeholder="Example: Choosing friends, lifestyle, opinions, trends..."
    )

    peer_pressure = st.checkbox(
        "Feeling pressure from friends or group?"
    )

    majority_opinion = st.selectbox(
        "Majority Opinion Around You",
        ["supportive", "neutral", "opposing"]
    )

    emotional_state = st.selectbox(
        "Your Emotional State",
        ["calm", "confused", "excited", "fear"]
    )

    confidence_level = st.selectbox(
        "Confidence in Your Own Decision",
        ["low", "medium", "high"]
    )

    st.divider()

    analyze = st.button("🔍 Analyze Social Decision")

    # -------- ANALYSIS --------
    if analyze:
        decision_data = {
            "decision_context": decision_context,
            "peer_pressure": peer_pressure,
            "majority_opinion": majority_opinion,
            "emotion": emotional_state,
            "confidence_level": confidence_level
        }

        bias_result = detect_bias(decision_data)
        score = calculate_decision_score(bias_result)
        suggestions = suggest_corrections(bias_result)

        st.subheader("📊 Analysis Result")
        st.metric("Decision Rationality Score", f"{score}/100")

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
