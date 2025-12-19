import json
from datetime import datetime
from quart import session
from typing import Any
from app.extensions import socketio
from app.services.chat_service import save_message, get_users_in_room
from app.worker import translate_message_task

# FIX: Use 'Any' to completely silence Pylance type errors for the socketio server.
# Pylance sometimes struggles to infer the AsyncServer type from the extension module.
server: Any = socketio

@server.on("join")
async def handle_join(sid, data):
    room = data["room"]
    username = session.get("user")
    
    if not username:
        return

    # Now valid because 'server' is Any (Pylance assumes it works)
    await server.enter_room(sid, room)
    
    await server.emit("message", {
        "user": "System", 
        "message": f"{username} has joined the chat",
        "type": "presence",
        "status": "online"
    }, room=room)

@server.on("leave")
async def handle_leave(sid, data):
    room = data["room"]
    username = session.get("user")
    
    if not username:
        return

    await server.leave_room(sid, room)
    
    await server.emit("message", {
        "user": "System", 
        "message": f"{username} has left the chat",
        "type": "presence",
        "status": "offline"
    }, room=room)

@server.on("message")
async def handle_message(sid, data):
    room = data["room"]
    message = data["message"]
    username = session.get("user")

    if not isinstance(username, str):
        return

    participants = room.split('_')[1:]
    
    # 1. Get users (Async)
    users_with_langs = await get_users_in_room(room)
    user_languages = {user["username"]: user["language"] for user in users_with_langs}

    # 2. Determine target language
    target_lang = "en"
    for user in participants:
        if user != username:
            target_lang = user_languages.get(user, "en")
            break
            
    # 3. Offload Translation
    try:
        # Note: We await the task result here for simplicity in this flow
        task = await translate_message_task.kiq(message, target_lang)
        result = await task.wait_result()
        translated_text = result.return_value
    except Exception:
        translated_text = message

    # 4. Save (Async)
    await save_message(username, message, room, translated_text)

    # 5. Broadcast
    await server.emit("message", {
        "user": username,
        "message": translated_text,
        "original_message": message,
        "timestamp": datetime.now().isoformat(),
        "type": "chat"
    }, room=room)