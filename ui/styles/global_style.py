import streamlit as st


def load_global_style():

    st.markdown("""
    <style>

    /* -------- PAGE BACKGROUND -------- */
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        background-attachment: fixed;
    }

    /* -------- GLOBAL TEXT COLOR -------- */
    body, p, h1, h2, h3, h4, h5, h6, span, label {
        color: #f1f5f9 !important;
    }

    /* -------- GLASS CONTENT PANEL -------- */
    .glass-card {
        background: rgba(255, 255, 255, 0.08);
        padding: 25px;
        border-radius: 15px;
        backdrop-filter: blur(12px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        margin-bottom: 25px;
    }

    /* -------- HERO BANNER -------- */
    .hero-banner {
        text-align: center;
        padding: 40px;
        border-radius: 18px;
        background: rgba(255,255,255,0.05);
        box-shadow: 0 0 25px rgba(0,0,0,0.4);
        margin-bottom: 30px;
    }

    /* -------- NAV BUTTON -------- */
    .stButton button {
        border-radius: 8px;
        background: linear-gradient(90deg, #ff7e5f, #feb47b);
        color: white;
        font-weight: bold;
        border: none;
    }

    </style>
    """, unsafe_allow_html=True)
