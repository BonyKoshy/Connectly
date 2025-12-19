from socketio import AsyncServer
from quart_rate_limiter import RateLimiter

# Initialize SocketIO with ASGI mode and Connection State Recovery
socketio = AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",
    logger=True,
    engineio_logger=True,
    connection_state_recovery={
        'max_disconnection_duration': 120 * 1000, # 2 minutes recovery window
        'skip_middlewares': True
    }
)

limiter = RateLimiter()