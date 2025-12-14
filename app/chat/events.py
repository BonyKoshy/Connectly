from flask import session
from flask_socketio import join_room, leave_room, send
from app.extensions import socketio
from app.services.chat_service import save_message, get_users_in_room
from deep_translator import GoogleTranslator
from datetime import datetime
import json

@socketio.on("join")
def handle_join(data):
    room = data["room"]
    username = session.get("user")
    join_room(room)
    send(json.dumps({
        "user": "System", 
        "message": f"{username} has joined the chat",
        "type": "presence",
        "status": "online"
    }), room=room)


@socketio.on("leave")
def handle_leave(data):
    room = data["room"]
    username = session.get("user")
    leave_room(room)
    send(json.dumps({
        "user": "System", 
        "message": f"{username} has left the chat",
        "type": "presence",
        "status": "offline"
    }), room=room)


@socketio.on("message")
def handle_message(data):
    room = data["room"]
    message = data["message"]
    username = session.get("user")

    save_message(username, message, room)

    participants = room.split('_')[1:]
    
    # Get users and their languages
    users_with_langs = get_users_in_room(room)
    user_languages = {user["username"]: user["language"] for user in users_with_langs}

    for user in participants:
        if user != username:  # Don't translate for sender
            target_lang = user_languages.get(user, "en")
            # Translate message
            try:
                translated_message = GoogleTranslator(source='auto', target=target_lang).translate(message)
            except Exception:
                translated_message = message # Fallback
        else:
            translated_message = message  # Sender gets the original message
    
        socketio.emit("message", {
            "user": username,
            "message": translated_message,
            "timestamp": datetime.now().isoformat(),
            "type": "chat"
        }, room=room)
