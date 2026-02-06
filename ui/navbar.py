import streamlit as st

def show_navbar():

    # Layout
    col1, col2 = st.columns([3, 5])

    # LEFT: LOGO / TITLE
    with col1:
        st.markdown("### 🧠 AI Decision Intelligence")

    # RIGHT: NAV ITEMS
    with col2:
        nav_cols = st.columns(4)

        # HOME
        if nav_cols[0].button("🏠 Home"):
            st.session_state.page = "Home"
            st.rerun()

        # SERVICE
        if nav_cols[1].button("🛠 Service"):
            st.session_state.page = "Service"
            st.rerun()

        # PROFILE (Login page if not logged in)
        if nav_cols[2].button("👤 Profile"):
            st.session_state.page = "Profile"
            st.rerun()

        # 🔐 LOGOUT (ONLY IF USER IS LOGGED IN)
        if st.session_state.user is not None:
            if nav_cols[3].button("🚪 Logout"):
                st.session_state.user = None
                st.session_state.page = "Home"
                st.rerun()
