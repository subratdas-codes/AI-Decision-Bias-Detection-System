import streamlit as st


def auth_card_start(title):

    st.markdown('<div class="auth-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="auth-title">{title}</div>', unsafe_allow_html=True)


def auth_card_end():

    st.markdown('</div>', unsafe_allow_html=True)


def load_auth_style():

    st.markdown("""
    <style>

    .auth-card {
        width: 420px;
        margin: auto;
        padding: 35px;
        background: rgba(255,255,255,0.08);
        backdrop-filter: blur(15px);
        border-radius: 18px;
        box-shadow: 0 0 30px rgba(0,0,0,0.4);
        margin-top: 60px;
    }

    .auth-title {
        text-align: center;
        font-size: 28px;
        font-weight: bold;
        color: white;
        text-shadow: 0 0 10px #00f2ff;
        margin-bottom: 20px;
    }

    </style>
    """, unsafe_allow_html=True)
