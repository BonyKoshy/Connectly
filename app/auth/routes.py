from quart import render_template, request, redirect, url_for, session, jsonify, flash
from app.services.auth_service import register_user, authenticate_user
from app.services.user_service import update_user_language
from . import auth

@auth.route("/register", methods=["GET", "POST"])
async def register():
    if request.method == "POST":
        # In Quart, request.form is a coroutine
        form = await request.form
        username = form["username"]
        password = form["password"]
        language = form["language"]

        # Service calls are now async
        success, message = await register_user(username, password, language)
        if success:
            return redirect(url_for("main.index"))
        else:
            await flash(message, 'error')
            return redirect(url_for('auth.register'))

    return await render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == "POST":
        form = await request.form
        username = form["username"]
        password = form["password"]
        
        # Async authentication
        user = await authenticate_user(username, password)
        if user:
            session["user"] = user["username"]
            session["language"] = user["language"]
            return redirect(url_for("chat.chat_list"))
        
        await flash('Invalid username or password', 'error')
        return redirect(url_for('auth.login'))
        
    return await render_template("login.html")

@auth.route("/logout")
async def logout():
    session.pop("user", None)
    return redirect(url_for("main.index"))

@auth.route("/update-language", methods=["POST"])
async def update_language():
    if "user" not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    # In Quart, get_json() is a coroutine
    data = await request.get_json()
    language = data.get("language")
    
    # Async service call
    success, message = await update_user_language(session["user"], language)
    if success:
         session["language"] = language
         return jsonify({"success": True})
    else:
         if message == "Invalid language":
             return jsonify({"error": "Invalid language"}), 400
         return jsonify({"error": message}), 500