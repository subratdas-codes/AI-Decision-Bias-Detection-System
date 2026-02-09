import streamlit as st

def show_service_page():

    st.markdown("## Our Services")
    st.caption("AI-powered decision intelligence modules")
    st.write("")

    # ---------- ROW 1 ----------
    col1, col2, col3 = st.columns(3)

    with col1:
        service_card(
            "🎓 Career Decision Support",
            "Choose careers using bias-aware AI analysis",
            "career"
        )

    with col2:
        service_card(
            "🧑‍💼 HR Hiring Bias Detection",
            "Detect bias in recruitment & hiring decisions",
            "hr"
        )

    with col3:
        service_card(
            "💰 Salary Decision Analysis",
            "Analyze salary decisions using AI & bias detection",
            "salary"
        )

    st.write("")

    # ---------- ROW 2 ----------
    col4, col5, col6 = st.columns(3)

    with col4:
        service_card(
            "🌍 Social Decision Analysis",
            "Understand social & group decision bias",
            "social"
        )

    with col5:
        service_card(
            "🏛 National Policy Simulation",
            "Simulate policy decisions & public impact",
            "policy"
        )

    with col6:
        service_card(
            "🧠 Custom Decision",
            "User-defined decision analysis",
            "custom"
        )


def service_card(title, desc, route):
    with st.container():
        st.markdown(
            f"""
            <div class="glass service-card">
                <h4>{title}</h4>
                <p style="font-size:14px;">{desc}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button("Explore", key=route, use_container_width=True):
            st.session_state.page = route
            st.rerun()
