import streamlit as st
import time
import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="xxxx",
        database="users"
    )

def delete_history_record(history_id):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM history WHERE history_id = %s", (history_id,))
        db.commit()
    finally:
        cursor.close()
        db.close()

def fetch_history(user_id):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT h.history_id, h.question, h.answer, h.timestamp, p.pdf_name
            FROM history h
            JOIN pdfs p ON h.pdf_id = p.pdf_id
            WHERE h.user_id = %s
            ORDER BY h.timestamp DESC
        """, (user_id,))
        records = cursor.fetchall()
        return records
    finally:
        cursor.close()
        db.close()

def history():
    st.header("History")
    
    if st.session_state.get("user") == "Guest":
        if "history" in st.session_state:
            for entry in st.session_state.history:
                st.write(f"**Question:** {entry['question']}")
                st.write(f"**Answer:** {entry['answer']}")
        else:
            st.write("No history available.")
    else:
        user_id = st.session_state.get("user_id")
        
        # Debugging: Print user_id to ensure it is set correctly
        # st.write(f"Debug: User ID = {user_id}")
        
        if user_id:
            records = fetch_history(user_id)

            # Debugging: Print records to see if they are fetched correctly
            # st.write(f"Debug: Fetched Records = {records}")

            if records:
                for record in records:
                    st.write(f"**Timestamp:** {record['timestamp']}")
                    st.write(f"**PDF Name:** {record['pdf_name']}")
                    st.write(f"**Question:** {record['question']}")
                    st.write(f"**Answer:** {record['answer']}")

                    bt=st.button(f"Delete 🗑️", key=f"delete_{record['history_id']}")
                if bt:
                    delete_history_record(record['history_id'])
                    st.experimental_rerun()
            else:
                st.write("No history available.")
        else:
            st.write("")

if __name__ == "__main__":
    history()