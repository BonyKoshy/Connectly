
import sqlite3
from app.db import get_db_connection
from datetime import datetime
from typing import List, Dict, Any

def get_chat_history(room: str) -> List[sqlite3.Row]: # type: ignore
    """Retrieves chat history for a specific room."""
    conn = get_db_connection()
    messages = conn.execute("SELECT user, message, timestamp FROM chats WHERE room = ? ORDER by timestamp ASC", (room,)).fetchall()
    conn.close()
    return messages

def save_message(username: str, message: str, room: str) -> None:
    """Saves a message to the database."""
    conn = get_db_connection()
    conn.execute("INSERT INTO chats (user, message, room) VALUES (?, ?, ?)", 
                (username, message, room))
    conn.commit()
    conn.close()

def search_users(query: str, current_user: str) -> List[Dict[str, Any]]:
    """Searches for users excluding the current user."""
    conn = get_db_connection()
    users = conn.execute(
        "SELECT username FROM users WHERE username LIKE ? AND username != ? LIMIT 10",
        (f"%{query}%", current_user)
    ).fetchall()
    conn.close()
    return [dict(user) for user in users]

def get_users_in_room(room: str) -> List[Dict[str, Any]]:
    """Retrieves users participating in a room."""
    participants = room.split('_')[1:]
    if len(participants) < 2: 
        return []
    
    conn = get_db_connection()
    users = conn.execute(
        "SELECT username, language FROM users WHERE username IN (?, ?)",
        (participants[0], participants[1])
    ).fetchall()
    conn.close()
    return [dict(user) for user in users]
