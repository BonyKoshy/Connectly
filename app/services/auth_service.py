import aiosqlite
from app.db import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

async def register_user(username, password):
    """Registers a new user asynchronously."""
    password_hash = generate_password_hash(password)
    
    conn = await get_db_connection()
    try:
        await conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                           (username, password_hash))
        await conn.commit()
        return True
    except aiosqlite.IntegrityError:
        return False
    finally:
        await conn.close()

async def authenticate_user(username, password):
    """Authenticates a user asynchronously."""
    conn = await get_db_connection()
    try:
        async with conn.execute("SELECT password FROM users WHERE username = ?", (username,)) as cursor:
            user = await cursor.fetchone()
        
        if user and check_password_hash(user['password'], password):
            return True
        return False
    finally:
        await conn.close()