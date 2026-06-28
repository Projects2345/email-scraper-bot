import sqlite3
import json
from config import DB_FILE

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            url TEXT,
            title TEXT,
            description TEXT,
            emails TEXT,
            phones TEXT,
            social_links TEXT,
            address TEXT,
            status TEXT DEFAULT 'new',
            notes TEXT DEFAULT '',
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def create_user(name, email, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def get_user_by_email(email):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

def save_result(result, user_id=None):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO results (user_id, url, title, description, emails, phones, social_links, address)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
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

def get_all_results(user_id=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if user_id:
        c.execute("SELECT * FROM results WHERE user_id = ? ORDER BY scraped_at DESC", (user_id,))
    else:
        c.execute("SELECT * FROM results ORDER BY scraped_at DESC")
    rows = c.fetchall()
    conn.close()
    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "user_id": row[1],
            "url": row[2],
            "title": row[3],
            "description": row[4],
            "emails": json.loads(row[5] or "[]"),
            "phones": json.loads(row[6] or "[]"),
            "social_links": json.loads(row[7] or "{}"),
            "address": json.loads(row[8] or "[]"),
            "status": row[9] or "new",
            "notes": row[10] or "",
            "scraped_at": row[11]
        })
    return results

def delete_result(result_id, user_id=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if user_id:
        c.execute("DELETE FROM results WHERE id = ? AND user_id = ?", (result_id, user_id))
    else:
        c.execute("DELETE FROM results WHERE id = ?", (result_id,))
    conn.commit()
    conn.close()

def update_result_status(result_id, status, notes, user_id=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    if user_id:
        c.execute("UPDATE results SET status = ?, notes = ? WHERE id = ? AND user_id = ?",
                  (status, notes, result_id, user_id))
    else:
        c.execute("UPDATE results SET status = ?, notes = ? WHERE id = ?",
                  (status, notes, result_id))
    conn.commit()
    conn.close()

def get_all_emails():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT emails, url, scraped_at FROM results")
    rows = c.fetchall()
    conn.close()
    all_emails = []
    for row in rows:
        emails = json.loads(row[0] or "[]")
        for email in emails:
            all_emails.append((email, row[1], row[2]))
    return all_emails
