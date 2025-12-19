import aiosqlite
from app.db import get_db_connection
from typing import List, Dict, Any, Optional

async def get_chat_history(room: str) -> List[Dict[str, Any]]:
    conn = await get_db_connection()
    async with conn.execute(
        "SELECT user, message, translated_message, timestamp FROM chats WHERE room = ? ORDER by timestamp ASC", 
        (room,)
    ) as cursor:
        rows = await cursor.fetchall()
    
    await conn.close()
    return [dict(row) for row in rows]

# Fixed: translated_message type hint includes None
async def save_message(username: str, message: str, room: str, translated_message: str | None = None) -> None:
    conn = await get_db_connection()
    await conn.execute(
        "INSERT INTO chats (user, message, translated_message, room) VALUES (?, ?, ?, ?)", 
        (username, message, translated_message, room)
    )
    await conn.commit()
    await conn.close()

async def get_users_in_room(room: str) -> List[Dict[str, Any]]:
    participants = room.split('_')[1:]
    if len(participants) < 2: 
        return []
    
    conn = await get_db_connection()
    # Note: Parametrized IN clause logic
    async with conn.execute(
        "SELECT username, language FROM users WHERE username = ? OR username = ?",
        (participants[0], participants[1])
    ) as cursor:
        rows = await cursor.fetchall()
    
    await conn.close()
    return [dict(row) for row in rows]