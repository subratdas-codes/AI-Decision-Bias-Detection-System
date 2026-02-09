import streamlit as st


def show_navbar():

    user_logged_in = st.session_state.get("user") is not None

    if user_logged_in:
        cols = st.columns([2.5, 1, 1, 1, 1, 1])
    else:
        cols = st.columns([2.5, 1, 1, 1, 1])

    col1 = cols[0]
    col2 = cols[1]
    col3 = cols[2]

    # LOGO
    with col1:
        st.markdown("🧠 **AI Decision Intelligence**")

    # HOME
    with col2:
        if st.button("Home"):
            st.session_state.page = "Home"

    # ABOUT
    with col3:
        if st.button("About"):
            st.session_state.page = "About"

    idx = 3

    # SERVICE (ONLY IF LOGGED IN)
    if user_logged_in:
        with cols[idx]:
            if st.button("Service"):
                st.session_state.page = "Service"
        idx += 1

    # PROFILE
    with cols[idx]:
        if st.button("Profile"):
            st.session_state.page = "Profile"
    idx += 1

    # ADMIN / LOGOUT
    with cols[idx]:
        if st.session_state.get("admin_logged_in"):
            if st.button("Logout"):
                st.session_state.admin_logged_in = False
                st.session_state.page = "Home"
        else:
            if st.button("Admin"):
                st.session_state.page = "Admin"
