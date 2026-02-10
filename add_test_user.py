import sqlite3

conn = sqlite3.connect("decision_history.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO users (username, email, is_banned)
VALUES (?, ?, ?)
""", ("testuser", "testuser@gmail.com", 0))

conn.commit()
conn.close()

print("✅ Test user added successfully")
