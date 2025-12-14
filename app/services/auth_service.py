from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db_connection
from typing import Optional, Dict, Any, Tuple
import sqlite3

def register_user(username: str, password: str, language: str) -> Tuple[bool, str]:
    """Registers a new user."""
    hashed_password = generate_password_hash(password)
    conn = get_db_connection()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                    (username, hashed_password))
        conn.execute("UPDATE users SET language = ? WHERE username = ?",
                    (language, username))
        conn.commit()
        conn.close()
        return True, "User registered successfully"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Username already exists"
    except Exception as e:
        conn.close()
        return False, str(e)

def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    """Authenticates a user and returns their details if successful."""
    conn = get_db_connection()
    user = conn.execute("SELECT username, password, COALESCE(language, 'en') as language FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        return {"username": user["username"], "language": user["language"]}
    return None
