import streamlit as st

def show_home_page():

    # ================= HERO SECTION =================
    st.markdown("""
    <div class="glass" style="text-align:center;">
        <h1>🧠 AI Decision Intelligence</h1>
        <p style="font-size:18px; margin-top:10px;">
            Make better decisions using AI-powered bias detection,
            behavioral insights, and intelligent recommendations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.write("")

    # CTA BUTTON
    col_cta1, col_cta2, col_cta3 = st.columns([2,1,2])
    with col_cta2:
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.page = "Profile"
            st.rerun()

    st.divider()

    # ================= FEATURES =================
    st.markdown("## 🔍 What This Platform Does")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("### 🔍 Bias Detection")
        st.write("Identify emotional and cognitive biases affecting decisions.")

    with c2:
        st.markdown("### 📊 Decision Scoring")
        st.write("Quantify decision quality using AI & ML models.")

    with c3:
        st.markdown("### 🤖 AI Assistant")
        st.write("Ask AI for guidance and unbiased suggestions.")

    with c4:
        st.markdown("### 📜 Decision History")
        st.write("Track and reflect on past decisions over time.")

    st.divider()

    # ================= HOW IT WORKS =================
    st.markdown("## ⚙️ How It Works")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("### 1️⃣ Input Decision")
        st.write("Provide context, emotions, and expectations.")

    with step2:
        st.markdown("### 2️⃣ Analyze Bias")
        st.write("AI evaluates patterns and detects bias.")

    with step3:
        st.markdown("### 3️⃣ Improve Choice")
        st.write("Get corrective suggestions and clarity.")

    st.divider()

    # ================= WHY US =================
    st.markdown("## 🌟 Why Use AI Decision Intelligence")

    st.write("""
    • Human-centered AI, not black-box automation  
    • Transparent bias explanations  
    • Supports rational and reflective decision-making  
    • Built for students, professionals, and researchers  
    """)

    st.divider()

    # ================= FINAL CTA =================
    st.markdown("""
    <div class="glass" style="text-align:center;">
        <h3>Start making unbiased decisions today</h3>
        <p>Your decisions shape your future — make them wisely.</p>
    </div>
    """, unsafe_allow_html=True)
