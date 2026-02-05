import streamlit as st
from utils.auth_manager import (
    change_password,
    delete_user_account,
    get_user_details
)


def profile_page(username):

    st.title("👤 User Profile")

    # ⭐ NEW → Show user details
    user_data = get_user_details(username)

    if user_data:
        st.write(f"### Username: {user_data[0]}")
        st.write(f"📧 Email: {user_data[1]}")
        st.write(f"📱 Mobile: {user_data[2]}")

    st.divider()

    # -------- CHANGE PASSWORD --------
    st.subheader("🔑 Change Password")

    old_pass = st.text_input("Old Password", type="password")
    new_pass = st.text_input("New Password", type="password")
    confirm_pass = st.text_input("Confirm Password", type="password")

    if st.button("Update Password"):

        if new_pass != confirm_pass:
            st.error("Passwords do not match")

        elif change_password(username, old_pass, new_pass):
            st.success("Password Updated")

        else:
            st.error("Old password incorrect")

    st.divider()

    # -------- DELETE ACCOUNT --------
    if st.button("🗑 Delete My Account"):

        delete_user_account(username)

        st.session_state.user = None
        st.success("Account Deleted")
        st.rerun()
