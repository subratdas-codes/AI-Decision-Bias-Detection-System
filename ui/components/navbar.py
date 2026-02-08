import streamlit as st
from ui.components.profile_menu import profile_menu


def navbar():

    col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])

    with col1:
        st.markdown("## 🧠 AI Decision System")

    with col2:
        if st.button("Home"):
            st.session_state.page = "Home"

    with col3:
        if st.button("About"):
            st.session_state.page = "About"

    # SERVICES ONLY AFTER LOGIN
    if st.session_state.user:
        with col4:
            if st.button("Services"):
                st.session_state.page = "Services"

    # PROFILE SECTION
    with col5:
        if st.session_state.user:
            profile_menu(st.session_state.user)
        else:
            if st.button("👤"):
                st.session_state.page = "Profile"

    st.divider()
