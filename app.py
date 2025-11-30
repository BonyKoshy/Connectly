from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from datetime import datetime

from flask_socketio import SocketIO, join_room, leave_room, send
from deep_translator import GoogleTranslator
import sqlite3

import sqlite3
import json

translator = GoogleTranslator()

app = Flask(__name__)
app.secret_key = "your_secret_key"
socketio = SocketIO(app)

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return render_template('400.html'), 400

@app.errorhandler(401)
def unauthorized(error):
    return render_template('401.html'), 401

@app.errorhandler(403)
def forbidden(error):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404



@app.route('/search_users_db')
def search_users_db():
    """Search for users by username"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])

    try:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute("SELECT username FROM users WHERE username LIKE ?", (f'%{query}%',))
        results = [{'username': row[0]} for row in cursor.fetchall()]
        conn.close()
        return jsonify(results)
    except Exception as e:
        print(f"Search error: {e}")
        return jsonify([])



# Database setup
def get_db_connection():
    conn = sqlite3.connect("chat.db")
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

init_db()

# Routes
@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("chat_list"))
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        language = request.form["language"]

        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                        (username, password))
            conn.execute("UPDATE users SET language = ? WHERE username = ?",
                        (language, username))
            conn.commit()
            conn.close()
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            conn.close()
            flash('Username already exists.', 'error')
            return redirect(url_for('register'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_db_connection()
        user = conn.execute("SELECT username, password, COALESCE(language, 'en') as language FROM users WHERE username = ? AND password = ?", (username, password)).fetchone()
        conn.close()
        if user:
            session["user"] = username
            session["language"] = user["language"]
            return redirect(url_for("chat_list"))
        flash('Invalid username or password', 'error')
        return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/filetransfer")
def filetransfer():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("filetransfer.html")

@app.route("/groups")
def groups():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("groups.html")

@app.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("profile.html", username=session["user"])    

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/update-language", methods=["POST"])
def update_language():
    if "user" not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    data = request.get_json()
    language = data.get("language")
    
    if not language or language not in ["en", "es", "fr", "de", "hi", "zh", "ja", "ko", "ar", "ru"]:
        return jsonify({"error": "Invalid language"}), 400
        
    conn = get_db_connection()
    try:
        conn.execute("UPDATE users SET language = ? WHERE username = ?", 
                    (language, session["user"]))
        conn.commit()
        session["language"] = language
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route("/search_users", methods=["GET"])
def search_users():
    if "user" not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    query = request.args.get("q", "")
    if not query:
        return jsonify([])
        
    conn = get_db_connection()
    users = conn.execute(
        "SELECT username FROM users WHERE username LIKE ? AND username != ? LIMIT 10",
        (f"%{query}%", session["user"])
    ).fetchall()
    conn.close()
    
    return jsonify([dict(user) for user in users])

@app.route("/chat_list")
def chat_list():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("chat_list.html", username=session["user"])

@app.route("/start_chat/<username>")
def start_chat(username):
    if "user" not in session:
        return redirect(url_for("index"))
        
    # Create a unique room name for the private chat
    participants = sorted([session["user"], username])
    room = f"private_{participants[0]}_{participants[1]}"
    
    return redirect(url_for("chat", room=room, receiver_name=username))



@app.route("/chat/<room>")
def chat(room):
    if "user" not in session:
        return redirect(url_for("index"))
    conn = get_db_connection()
    messages = conn.execute("SELECT user, message, timestamp FROM chats WHERE room = ? ORDER by timestamp ASC", (room,)).fetchall()
    conn.close()
    
    # Extract receiver's name from room name
    participants = room.split('_')[1:]
    receiver_name = participants[0] if participants[0] != session["user"] else participants[1]
    
    return render_template("chat.html", 
                          username=session["user"], 
                          room=room, 
                          messages=messages,
                          receiver_name=receiver_name)


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

    conn = get_db_connection()

    # Store the original message
    conn.execute("INSERT INTO chats (user, message, room) VALUES (?, ?, ?)", 
                (username, message, room))
    conn.commit()

    # Get all users in the room and their language preferences
    participants = room.split('_')[1:]
    users = conn.execute(
        "SELECT username, language FROM users WHERE username IN (?, ?)",
        (participants[0], participants[1])
    ).fetchall()
    conn.close()

    # Convert list of tuples to a dictionary {username: language}
    user_languages = {user["username"]: user["language"] for user in users}

    for user in participants:
        if user != username:  # Don't translate for sender
            target_lang = user_languages.get(user, "en")
            translated_message = GoogleTranslator(source='auto', target=target_lang).translate(message)
        else:
            translated_message = message  # Sender gets the original message
    
        socketio.emit("message", {
            "user": username,
            "message": translated_message,
            "timestamp": datetime.now().isoformat(),
            "type": "chat"
        }, room=room) # type: ignore



if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)


