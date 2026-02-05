import sqlite3
import hashlib


# -------- DATABASE CONNECTION --------
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()


# -------- CREATE USERS TABLE --------
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    username TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    mobile TEXT UNIQUE,
    password TEXT
)
""")

conn.commit()


# =====================================
# ⭐ PASSWORD HASH
# =====================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# =====================================
# ⭐ SIGNUP
# =====================================
def signup(username, email, mobile, password):

    try:
        cursor.execute("""
        INSERT INTO users VALUES (?, ?, ?, ?)
        """, (
            username,
            email,
            mobile,
            hash_password(password)
        ))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False


# =====================================
# ⭐ LOGIN
# =====================================
def login(identifier, password):

    cursor.execute("""
    SELECT username FROM users
    WHERE (username=? OR email=? OR mobile=?)
    AND password=?
    """, (
        identifier,
        identifier,
        identifier,
        hash_password(password)
    ))

    result = cursor.fetchone()

    if result:
        return result[0]

    return None


# =====================================
# ⭐ GET USER DETAILS
# =====================================
def get_user_details(username):

    cursor.execute("""
    SELECT username, email, mobile
    FROM users WHERE username=?
    """, (username,))

    return cursor.fetchone()


# =====================================
# ⭐ CHANGE PASSWORD
# =====================================
def change_password(username, old_pass, new_pass):

    cursor.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    )

    result = cursor.fetchone()

    if result and result[0] == hash_password(old_pass):

        cursor.execute("""
        UPDATE users SET password=? WHERE username=?
        """, (
            hash_password(new_pass),
            username
        ))

        conn.commit()
        return True

    return False


# =====================================
# ⭐ UPDATE EMAIL
# =====================================
def update_email(username, new_email):

    try:
        cursor.execute("""
        UPDATE users SET email=? WHERE username=?
        """, (new_email, username))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False


# =====================================
# ⭐ UPDATE MOBILE
# =====================================
def update_mobile(username, new_mobile):

    try:
        cursor.execute("""
        UPDATE users SET mobile=? WHERE username=?
        """, (new_mobile, username))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False


# =====================================
# ⭐ DELETE ACCOUNT
# =====================================
def delete_user_account(username):

    cursor.execute("""
    DELETE FROM users WHERE username=?
    """, (username,))

    conn.commit()


# =====================================
# ⭐ ADMIN – GET ALL USERS
# =====================================
def get_all_users():

    cursor.execute("""
    SELECT username, email, mobile FROM users
    """)

    return cursor.fetchall()
