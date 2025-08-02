import sqlite3

DB_NAME = 'url_shortener.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT UNIQUE NOT NULL,
            original_url TEXT NOT NULL,
            visit_count INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def insert_url(short_code, original_url):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO urls (short_code, original_url)
        VALUES (?, ?)
    ''', (short_code, original_url))
    conn.commit()
    conn.close()

def get_url(short_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT original_url, visit_count FROM urls WHERE short_code = ?
    ''', (short_code,))
    row = c.fetchone()
    conn.close()
    return row

def increment_visit_count(short_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE urls SET visit_count = visit_count + 1 WHERE short_code = ?
    ''', (short_code,))
    conn.commit()
    conn.close()

def get_stats(short_code):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        SELECT original_url, visit_count FROM urls WHERE short_code = ?
    ''', (short_code,))
    row = c.fetchone()
    conn.close()
    return row
