import streamlit as st

# =====================================
# 🔻 FOOTER RENDER FUNCTION (ADDED)
# =====================================
def render_footer():
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center;'>© PHB2 | AI Decision Bias Detection</p>",
        unsafe_allow_html=True
    )
import streamlit as st

# =====================================
# 🔻 GLOBAL FOOTER COMPONENT
# =====================================
def footer():
    st.markdown("---")
    st.markdown(
        "<p style='text-align:center; font-size:14px;'>"
        "© PHB2 | AI Decision Bias Detection System"
        "</p>",
        unsafe_allow_html=True
    )
