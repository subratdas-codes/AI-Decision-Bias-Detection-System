import streamlit as st
from utils.history_manager import load_history, delete_record, delete_all


def history_page(username):

    st.subheader("📜 Your Decision History")

    history_df = load_history(username)

    if not history_df.empty:

        st.dataframe(history_df, use_container_width=True)

        record_id = st.number_input("Enter Record ID to Delete", min_value=0)

        if st.button("Delete Selected Record"):
            delete_record(record_id)
            st.rerun()

        if st.button("Clear All History"):
            delete_all(username)
            st.rerun()

    else:
        st.write("No history available yet.")
