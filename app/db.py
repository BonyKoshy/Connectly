import sqlite3
from flask import g

DATABASE = 'chat.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute('PRAGMA journal_mode=WAL') # Enable Write-Ahead Logging
    conn.execute('PRAGMA foreign_keys=ON') # Enable Foreign Keys
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Ensure the language column exists in existing users table
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN language TEXT DEFAULT 'en'")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        message TEXT NOT NULL,
        translated_message TEXT,
        room TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )""")
    try:
        cursor.execute("ALTER TABLE chats ADD COLUMN translated_message TEXT")
        conn.commit()
    except sqlite3.OperationalError:
        pass  # Column already exists
    conn.commit()
    conn.close()
