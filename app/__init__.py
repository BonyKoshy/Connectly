from flask import Flask
from config import config
from app.extensions import socketio, csrf, limiter

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    socketio.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    
    # Register Blueprints
    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.chat import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)
    
    # Error handlers
    from flask import render_template
    
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
        
    @app.after_request
    def add_security_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-eval' https://cdn.jsdelivr.net https://www.google.com https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; font-src 'self' https://cdn.jsdelivr.net; frame-src 'self' https://www.google.com; object-src 'none';"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app
