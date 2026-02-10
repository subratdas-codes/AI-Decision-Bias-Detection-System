import sqlite3

def get_connection():
    return sqlite3.connect("decision_history.db", check_same_thread=False)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # USERS TABLE (MATCHES ADMIN QUERY)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        role TEXT DEFAULT 'user',
        is_banned INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # HISTORY TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        decision TEXT,
        emotion TEXT,
        score INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
