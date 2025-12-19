from quart import render_template, redirect, url_for, session
from . import main

@main.route("/")
async def index():
    if "user" in session:
        return redirect(url_for("chat.chat_list"))
    return await render_template("index.html")

@main.route("/filetransfer")
async def filetransfer():
    if "user" not in session:
        return redirect(url_for("main.index"))
    return await render_template("filetransfer.html")

@main.route("/groups")
async def groups():
    if "user" not in session:
        return redirect(url_for("main.index"))
    return await render_template("groups.html")

@main.route("/profile")
async def profile():
    if "user" not in session:
        return redirect(url_for("main.index"))
    return await render_template("profile.html", username=session["user"])