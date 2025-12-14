from flask import render_template, request, redirect, url_for, session, jsonify, flash
from app.services.auth_service import register_user, authenticate_user
from app.services.user_service import update_user_language
from . import auth

@auth.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        language = request.form["language"]

        success, message = register_user(username, password, language)
        if success:
            return redirect(url_for("main.index"))
        else:
            flash(message, 'error')
            return redirect(url_for('auth.register'))

    return render_template("register.html")

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        user = authenticate_user(username, password)
        if user:
            session["user"] = user["username"]
            session["language"] = user["language"]
            return redirect(url_for("chat.chat_list"))
        flash('Invalid username or password', 'error')
        return redirect(url_for('auth.login'))
    return render_template("login.html")

@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("main.index"))

@auth.route("/update-language", methods=["POST"])
def update_language():
    if "user" not in session:
        return jsonify({"error": "Not authenticated"}), 401
        
    data = request.get_json()
    language = data.get("language")
    
    success, message = update_user_language(session["user"], language)
    if success:
         session["language"] = language
         return jsonify({"success": True})
    else:
         if message == "Invalid language":
             return jsonify({"error": "Invalid language"}), 400
         return jsonify({"error": message}), 500
