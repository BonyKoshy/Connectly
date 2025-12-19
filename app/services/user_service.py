import aiosqlite
from app.db import get_db_connection
from typing import List, Dict, Any, Optional

async def search_users(query: str, current_user: str) -> List[Dict[str, Any]]:
    """Searches for users excluding the current user."""
    conn = await get_db_connection()
    try:
        async with conn.execute(
            "SELECT username FROM users WHERE username LIKE ? AND username != ? LIMIT 10",
            (f"%{query}%", current_user)
        ) as cursor:
            users = await cursor.fetchall()
        return [dict(user) for user in users]
    finally:
        await conn.close()

async def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    conn = await get_db_connection()
    try:
        async with conn.execute("SELECT * FROM users WHERE username = ?", (username,)) as cursor:
            user = await cursor.fetchone()
        if user:
            return dict(user)
        return None
    finally:
        await conn.close()

async def update_user_language(username: str, language: str) -> tuple[bool, str]:
    conn = await get_db_connection()
    try:
        # Check if user exists first
        async with conn.execute("SELECT 1 FROM users WHERE username = ?", (username,)) as cursor:
             if not await cursor.fetchone():
                 return False, "User not found"

        await conn.execute("UPDATE users SET language = ? WHERE username = ?", (language, username))
        await conn.commit()
        return True, "Language updated"
    except Exception as e:
        return False, str(e)
    finally:
        await conn.close()