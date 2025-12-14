from flask import render_template, redirect, url_for, session
from . import main

@main.route("/")
def index():
    if "user" in session:
        return redirect(url_for("chat.chat_list"))
    return render_template("index.html")

@main.route("/filetransfer")
def filetransfer():
    if "user" not in session:
        return redirect(url_for("main.index"))
    return render_template("filetransfer.html")

@main.route("/groups")
def groups():
    if "user" not in session:
        return redirect(url_for("main.index"))
    return render_template("groups.html")

@main.route("/profile")
def profile():
    if "user" not in session:
        return redirect(url_for("main.index"))
    return render_template("profile.html", username=session["user"])
