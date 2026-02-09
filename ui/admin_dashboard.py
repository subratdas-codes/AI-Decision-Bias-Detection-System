import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px


# -------- DATABASE CONNECTION --------
conn = sqlite3.connect("decision_history.db", check_same_thread=False)


# -------- LOAD ALL DECISION DATA --------
def load_all_data():
    query = "SELECT * FROM history"
    return pd.read_sql_query(query, conn)


# =====================================
# ⭐ ADMIN DASHBOARD
# =====================================
def admin_dashboard():

    # 🔐 ADMIN SESSION PROTECTION
    if not st.session_state.get("admin_logged_in"):
        st.error("Unauthorized Access ❌")
        st.stop()

    # -------- HEADER + LOGOUT --------
    col_left, col_right = st.columns([8, 2])

    with col_left:
        st.title("🛠 Admin Analytics Dashboard")

    with col_right:
        if st.button("🚪 Logout"):
            st.session_state["admin_logged_in"] = False
            st.rerun()

    st.divider()

    # -------- LOAD DATA --------
    df = load_all_data()

    if df.empty:
        st.warning("No decision data available.")
        return

    # -------- SYSTEM METRICS --------
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

    # -------- RAW DATA --------
    with st.expander("📄 View Raw Dataset"):
        st.dataframe(df, use_container_width=True)
