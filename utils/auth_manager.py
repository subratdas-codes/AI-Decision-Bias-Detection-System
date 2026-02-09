import sqlite3
import hashlib
import os

# =====================================
# 📂 DATABASE PATH (FIXED)
# =====================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "users.db")

# =====================================
# 🔐 PASSWORD HASH
# =====================================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# =====================================
# ⭐ ADMIN CREDENTIALS (FIXED)
# =====================================
ADMIN_CREDENTIALS = {
    "user_id": "Admin",
    "email": "byteconnect360@gmail.com",
    "mobile": "9090535566",
    "password": hash_password("admin123")
}

# =====================================
# 🗄 DATABASE CONNECTION
# =====================================
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# =====================================
# CREATE USERS TABLE
# =====================================
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
# CHECK USER EXISTS
# =====================================
def user_exists(username=None, email=None, mobile=None):

    if username:
        cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            return True

    if email:
        cursor.execute("SELECT 1 FROM users WHERE email=?", (email,))
        if cursor.fetchone():
            return True

    if mobile:
        cursor.execute("SELECT 1 FROM users WHERE mobile=?", (mobile,))
        if cursor.fetchone():
            return True

    return False

# =====================================
# SIGNUP
# =====================================
def signup(username, email, mobile, password):

    try:
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?, ?)",
            (username, email, mobile, hash_password(password))
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

# =====================================
# LOGIN (USERNAME / EMAIL / MOBILE)
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
    return result[0] if result else None

# =====================================
# GET USER DETAILS
# =====================================
def get_user_details(username):

    cursor.execute("""
        SELECT username, email, mobile
        FROM users WHERE username=?
    """, (username,))

    return cursor.fetchone()

# =====================================
# CHANGE PASSWORD
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
        """, (hash_password(new_pass), username))
        conn.commit()
        return True

    return False

# =====================================
# UPDATE EMAIL
# =====================================
def update_email(username, new_email):

    try:
        cursor.execute(
            "UPDATE users SET email=? WHERE username=?",
            (new_email, username)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

# =====================================
# UPDATE MOBILE
# =====================================
def update_mobile(username, new_mobile):

    try:
        cursor.execute(
            "UPDATE users SET mobile=? WHERE username=?",
            (new_mobile, username)
        )
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

# =====================================
# DELETE USER ACCOUNT
# =====================================
def delete_user_account(username):

    cursor.execute(
        "DELETE FROM users WHERE username=?",
        (username,)
    )
    conn.commit()

# =====================================
# GET USERNAME BY EMAIL
# =====================================
def get_username_by_email(email):

    cursor.execute(
        "SELECT username FROM users WHERE email=?",
        (email,)
    )
    return cursor.fetchall()

# =====================================
# ⭐ ADMIN LOGIN (SEPARATE FROM USERS)
# =====================================
def admin_login(user_id, email, mobile, password):

    return (
        user_id == ADMIN_CREDENTIALS["user_id"]
        and email == ADMIN_CREDENTIALS["email"]
        and mobile == ADMIN_CREDENTIALS["mobile"]
        and hash_password(password) == ADMIN_CREDENTIALS["password"]
    )

# =====================================
# 🔑 RESET PASSWORD BY EMAIL (ADDED)
# =====================================
def reset_password_by_email(email, new_password):
    """
    Reset user password using email (used in Forgot Password flow)
    """

    try:
        cursor.execute(
            "UPDATE users SET password=? WHERE email=?",
            (hash_password(new_password), email)
        )
        conn.commit()

        # Check if any row was updated
        if cursor.rowcount == 0:
            return False

        return True

    except Exception as e:
        print("Reset password error:", e)
        return False
