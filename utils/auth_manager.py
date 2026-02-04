import sqlite3
import hashlib

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    password TEXT
)
""")

conn.commit()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def signup(username, password):
    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False


def login(username, password):
    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, hash_password(password))
    )
    return cursor.fetchone()
