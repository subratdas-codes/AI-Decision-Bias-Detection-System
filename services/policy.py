import streamlit as st

from rule_engine.bias_rules import detect_bias
from ml_model.decision_scoring import calculate_decision_score
from utils.correction_engine import suggest_corrections


def show_policy_service():

    st.markdown("## 🏛 National Policy Decision Simulation")
    st.write(
        "Simulate large-scale policy decisions and analyze potential bias and impact."
    )

    st.divider()

    # -------- INPUTS --------
    policy_title = st.text_input(
        "Policy Title",
        placeholder="Example: Education Reform Policy"
    )

    policy_description = st.text_area(
        "Policy Description",
        placeholder="Describe the policy goals and approach..."
    )

    affected_group = st.selectbox(
        "Primary Affected Group",
        ["students", "employees", "citizens", "businesses", "mixed"]
    )

    public_sentiment = st.selectbox(
        "Current Public Sentiment",
        ["positive", "neutral", "negative"]
    )

    decision_urgency = st.selectbox(
        "Decision Urgency",
        ["low", "medium", "high"]
    )

    st.divider()

    analyze = st.button("🔍 Simulate Policy Decision")

    # -------- ANALYSIS --------
    if analyze:
        decision_data = {
            "policy_title": policy_title,
            "policy_description": policy_description,
            "affected_group": affected_group,
            "public_sentiment": public_sentiment,
            "decision_urgency": decision_urgency
        }

        bias_result = detect_bias(decision_data)
        score = calculate_decision_score(bias_result)
        suggestions = suggest_corrections(bias_result)

        st.subheader("📊 Simulation Result")
        st.metric("Policy Rationality Score", f"{score}/100")

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
