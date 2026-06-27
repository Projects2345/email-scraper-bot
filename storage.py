import sqlite3
import csv
import os
from config import OUTPUT_CSV, DB_FILE

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            source_url TEXT,
            found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_email(email, source_url):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT OR IGNORE INTO emails (email, source_url) VALUES (?, ?)",
                  (email, source_url))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

    file_exists = os.path.isfile(OUTPUT_CSV)
    with open(OUTPUT_CSV, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Email', 'Source URL'])
        writer.writerow([email, source_url])

def get_all_emails():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT email, source_url, found_at FROM emails ORDER BY found_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows