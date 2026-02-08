import streamlit as st
from utils.chat_assistant import generate_chat_response


def chatbot_page():

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    st.subheader("🤖 AI Chat Decision Assistant")

    user_msg = st.text_input("Ask AI about your decision")

    if st.button("Send Message"):
        if user_msg:
            reply = generate_chat_response(user_msg)
            st.session_state.chat_history.append(("You", user_msg))
            st.session_state.chat_history.append(("AI", reply))

    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.write(f"👤 **You:** {msg}")
        else:
            st.write(f"🤖 **AI:** {msg}")
