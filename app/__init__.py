import secrets
from quart import Quart, render_template, g
from socketio import ASGIApp
from config import config
from app.extensions import socketio, limiter

def create_app(config_name='default'):
    app = Quart(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(config[config_name])

    # Initialize Extensions
    limiter.init_app(app)
    
    app_asgi = ASGIApp(socketio, app)

    # Register Blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)

    @app.before_request
    async def create_nonce():
        # Generate a unique nonce for this request
        g.nonce = secrets.token_urlsafe(16)

    @app.after_request
    def add_security_headers(response):
        # FIX: Explicitly allow the domains causing your errors
        csp_policy = (
            f"default-src 'self'; "
            f"script-src 'self' 'nonce-{g.nonce}' https://cdn.jsdelivr.net https://cdn.tailwindcss.com; "
            # Added https://unpkg.com here for Boxicons
            f"style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdn.tailwindcss.com https://fonts.googleapis.com https://unpkg.com; "
            # Added https://cdn.jsdelivr.net and https://unpkg.com here for Fonts
            f"font-src 'self' https://fonts.gstatic.com https://cdn.jsdelivr.net https://unpkg.com; "
            f"img-src 'self' data:; "
            f"connect-src 'self' ws: wss:;"
        )
        response.headers['Content-Security-Policy'] = csp_policy
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response

    @app.errorhandler(404)
    async def not_found(error):
        return await render_template('error.html', error_code=404, title="Not Found"), 404

    return app_asgi