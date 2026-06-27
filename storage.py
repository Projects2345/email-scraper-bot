import sqlite3
import os
import json
from config import DB_FILE

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            title TEXT,
            description TEXT,
            emails TEXT,
            phones TEXT,
            social_links TEXT,
            address TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_result(result):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO results (url, title, description, emails, phones, social_links, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            result["url"],
            result["title"],
            result["description"],
            json.dumps(result["emails"]),
            json.dumps(result["phones"]),
            json.dumps(result["social_links"]),
            json.dumps(result["address"])
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"DB Error: {e}")

def get_all_results():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM results ORDER BY scraped_at DESC")
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "url": row[1],
            "title": row[2],
            "description": row[3],
            "emails": json.loads(row[4]),
            "phones": json.loads(row[5]),
            "social_links": json.loads(row[6]),
            "address": json.loads(row[7]),
            "scraped_at": row[8]
        })
    return results

def delete_result(result_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM results WHERE id = ?", (result_id,))
    conn.commit()
    conn.close()