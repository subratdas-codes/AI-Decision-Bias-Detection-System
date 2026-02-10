import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


# =====================================
# DATABASE CONNECTIONS
# =====================================
conn = sqlite3.connect("decision_history.db", check_same_thread=False)
users_conn = sqlite3.connect("decision_history.db", check_same_thread=False)


# =====================================
# LOAD DECISION HISTORY
# =====================================
def load_all_data():
    query = "SELECT * FROM history"
    return pd.read_sql_query(query, conn)


def load_all_users():
    query = """
    SELECT username, email, is_banned
    FROM users
    """
    return pd.read_sql_query(query, users_conn)


# =====================================
# ADMIN DASHBOARD
# =====================================
def admin_dashboard():

    # 🔐 ADMIN SESSION PROTECTION
    if not (
        st.session_state.get("is_admin")
        or st.session_state.get("admin_logged_in")
    ):
        st.error("Unauthorized Access ❌")
        st.stop()

    # -------- HEADER + LOGOUT --------
    col_left, col_right = st.columns([8, 2])

    with col_left:
        st.title("🛠 Admin Analytics Dashboard")

    with col_right:
        if st.button("🚪 Logout"):
            st.session_state.is_admin = False
            st.session_state.admin_logged_in = False
            st.session_state.username = None
            st.session_state.page = "Home"
            st.rerun()

    st.divider()

    # =====================================
    # ANALYTICS SECTION
    # =====================================
    df = load_all_data()

    if df.empty:
        st.warning("No decision data available.")
    else:
        total_users = df["username"].nunique()
        total_decisions = len(df)
        avg_score = int(df["score"].mean())

        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Total Users", total_users)
        col2.metric("📊 Total Decisions", total_decisions)
        col3.metric("⭐ Average Decision Score", avg_score)

        st.divider()

        # -------- USER ACTIVITY --------
        st.subheader("👤 User Activity")

        user_counts = df["username"].value_counts().reset_index()
        user_counts.columns = ["User", "Decisions"]

        fig1 = px.bar(
            user_counts,
            x="User",
            y="Decisions",
            title="User Decision Count"
        )
        st.plotly_chart(fig1, use_container_width=True)

        # -------- SCORE DISTRIBUTION --------
        st.subheader("📊 Decision Score Distribution")

        fig2 = px.histogram(
            df,
            x="score",
            nbins=10,
            title="Decision Score Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

        # -------- EMOTION TREND --------
        st.subheader("😊 Emotional Decision Trend")

        emotion_counts = df["emotion"].value_counts().reset_index()
        emotion_counts.columns = ["Emotion", "Count"]

        fig3 = px.pie(
            emotion_counts,
            names="Emotion",
            values="Count",
            title="Emotion Distribution"
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        with st.expander("📄 View Raw Decision Dataset"):
            st.dataframe(df, use_container_width=True)

    # =====================================
    # USER MANAGEMENT SECTION
    # =====================================
    st.header("👥 User Management")

    users_df = load_all_users()

    if users_df.empty:
        st.warning("No users found.")
        return

    st.dataframe(users_df, use_container_width=True)

    # -------- SELECT USER --------
    selected_user = st.selectbox(
        "Select User",
        users_df["username"]
    )

    user_row = users_df[users_df["username"] == selected_user].iloc[0]

    # -------- EDIT USER --------
    st.subheader("✏️ Edit User Details")

    new_email = st.text_input("Email", user_row["email"])

    if st.button("Update User"):
        users_conn.execute(
            "UPDATE users SET email=? WHERE username=?",
            (new_email, selected_user)
        )
        users_conn.commit()
        st.success("User updated successfully ✅")
        st.rerun()

    # -------- BAN / UNBAN USER --------
    st.subheader("🚫 Ban / Unban User")

    if user_row["is_banned"] == 0:
        if st.button("Ban User"):
            users_conn.execute(
                "UPDATE users SET is_banned=1 WHERE username=?",
                (selected_user,)
            )
            users_conn.commit()
            st.warning("User banned 🚫")
            st.rerun()
    else:
        if st.button("Unban User"):
            users_conn.execute(
                "UPDATE users SET is_banned=0 WHERE username=?",
                (selected_user,)
            )
            users_conn.commit()
            st.success("User unbanned ✅")
            st.rerun()

    # -------- DELETE USER --------
    st.subheader("🗑 Delete User")

    confirm = st.checkbox("I understand this action is permanent")

    if confirm:
        if st.button("Delete User Permanently"):
            users_conn.execute(
                "DELETE FROM users WHERE username=?",
                (selected_user,)
            )
            users_conn.execute(
                "DELETE FROM history WHERE username=?",
                (selected_user,)
            )
            users_conn.commit()
            st.success("User deleted permanently 💀")
            st.rerun()
