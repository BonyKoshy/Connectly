import asyncio
from typing import cast, Any
from hypercorn.config import Config
from hypercorn.asyncio import serve
from app import create_app

# Create the ASGI application
app = create_app()

if __name__ == "__main__":
    config = Config()
    config.bind = ["localhost:5000"]
    config.use_reloader = True
    config.worker_class = "asyncio"
    
    # FIX: Cast 'app' to Any to silence Pylance error about ASGIApp vs Framework
    # The ASGIApp from python-socketio IS compatible, but the type stubs mismatch.
    asyncio.run(serve(cast(Any, app), config))