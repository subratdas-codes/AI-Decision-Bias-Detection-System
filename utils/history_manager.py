import sqlite3
import pandas as pd

conn = sqlite3.connect("decision_history.db", check_same_thread=False)
cursor = conn.cursor()

# -------- CREATE TABLE --------
cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    salary INTEGER,
    emotion TEXT,
    recent_event BOOLEAN,
    ignored_options BOOLEAN,
    prediction TEXT,
    score INTEGER
)
""")

conn.commit()


# -------- SAVE HISTORY --------
def save_history(username, record):

    cursor.execute("""
    INSERT INTO history 
    (username, salary, emotion, recent_event, ignored_options, prediction, score)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        record["Salary"],
        record["Emotion"],
        record["Recent Event"],
        record["Ignored Options"],
        record["Prediction"],
        record["Score"]
    ))

    conn.commit()


# -------- LOAD HISTORY --------
def load_history(username):

    cursor.execute("""
    SELECT id, salary, emotion, recent_event, ignored_options, prediction, score
    FROM history
    WHERE username=?
    """, (username,))

    data = cursor.fetchall()

    columns = [
        "ID",
        "Salary",
        "Emotion",
        "Recent Event",
        "Ignored Options",
        "Prediction",
        "Score"
    ]

    return pd.DataFrame(data, columns=columns)


# -------- DELETE SINGLE RECORD --------
def delete_record(record_id):

    cursor.execute("""
    DELETE FROM history WHERE id=?
    """, (record_id,))

    conn.commit()


# -------- DELETE ALL USER HISTORY --------
def delete_all(username):

    cursor.execute("""
    DELETE FROM history WHERE username=?
    """, (username,))

    conn.commit()
