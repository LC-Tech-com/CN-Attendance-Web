import sqlite3
import os

# Build absolute DB path inside "database" folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "database")
DB_NAME = os.path.join(DB_FOLDER, "attendance.db")

# Ensure database folder exists
if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print(f"✅ Database initialized at {DB_NAME}")

if __name__ == "__main__":
    init_db()
