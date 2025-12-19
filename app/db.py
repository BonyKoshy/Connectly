import aiosqlite
import os
from config import Config

DATABASE = Config.DB_PATH

async def get_db_connection():
    conn = await aiosqlite.connect(DATABASE)
    await conn.execute('PRAGMA journal_mode=WAL') 
    await conn.execute('PRAGMA foreign_keys=ON')
    conn.row_factory = aiosqlite.Row
    return conn

async def init_db():
    async with aiosqlite.connect(DATABASE) as conn:
        await conn.execute('PRAGMA journal_mode=WAL')
        
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            language TEXT DEFAULT 'en'
        )""")
        
        await conn.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            translated_message TEXT,
            room TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        
        await conn.commit()
        print(f"Database initialized at {DATABASE}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(init_db())