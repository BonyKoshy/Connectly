from app import create_app
from app.extensions import socketio
from app.db import init_db

app = create_app('development')

if __name__ == "__main__":
    init_db()
    socketio.run(app, host="127.0.0.1", port=5000, debug=True)
