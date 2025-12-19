from quart import render_template, request, redirect, url_for, session, jsonify
from app.services.chat_service import get_chat_history
from app.services.user_service import search_users 
from . import chat

@chat.route('/search_users_db')
async def search_users_db():
    """Search for users by username"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    try:
        results = await search_users(query, "IMPOSSIBLE_USER_XYZ")
        return jsonify(results)
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify([])

@chat.route("/search_users", methods=["GET"])
async def search_users_route():
    if "user" not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
        
    users = await search_users(query, session["user"])
    return jsonify(users)

@chat.route("/chat_list")
async def chat_list():
    if "user" not in session:
        return redirect(url_for("main.index"))
    return await render_template("chat_list.html", username=session["user"])

@chat.route("/start_chat/<username>")
async def start_chat(username):
    if "user" not in session:
        return redirect(url_for("main.index"))
        
    # Create a unique room name for the private chat
    participants = sorted([session["user"], username])
    room = f"private_{participants[0]}_{participants[1]}"
    
    return redirect(url_for("chat.render_chat_room", room=room, receiver_name=username))

# FIX: Renamed function from 'chat' to 'render_chat_room' to avoid collision with Blueprint 'chat'
@chat.route("/chat/<room>")
async def render_chat_room(room):
    if "user" not in session:
        return redirect(url_for("main.index"))
        
    messages = await get_chat_history(room)
    
    # Extract receiver's name from room name
    participants = room.split('_')[1:]
    
    if len(participants) < 2:
        receiver_name = "Unknown"
    else:
        receiver_name = participants[0] if participants[0] != session["user"] else participants[1]
    
    return await render_template("chat.html", 
                          username=session["user"], 
                          room=room, 
                          messages=messages,
                          receiver_name=receiver_name)