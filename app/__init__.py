from flask import Flask
from config import config
from app.extensions import socketio, csrf, limiter

def create_app(config_name='default'):
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
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
        return render_template('error.html', error_code=400, error_title="Bad Request", error_message="The browser (or proxy) sent a request that this server could not understand."), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return render_template('error.html', error_code=401, error_title="Unauthorized", error_message="You must be logged in to access this page."), 401

    @app.errorhandler(403)
    def forbidden(error):
        return render_template('error.html', error_code=403, error_title="Forbidden", error_message="You do not have permission to access this resource."), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html', error_code=404, error_title="Page Not Found", error_message="The requested URL was not found on the server."), 404
        
    @app.after_request
    def add_security_headers(response):
        response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-eval' 'unsafe-inline' https://cdn.jsdelivr.net https://www.google.com https://www.gstatic.com https://translate.google.com https://translate.googleapis.com https://translate-pa.googleapis.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://unpkg.com https://fonts.googleapis.com https://translate.googleapis.com https://www.gstatic.com; font-src 'self' https://cdn.jsdelivr.net https://unpkg.com https://fonts.gstatic.com; connect-src 'self' https://translate.googleapis.com https://translate-pa.googleapis.com; frame-src 'self' https://www.google.com; img-src 'self' data: https://www.google.com https://www.gstatic.com https://translate.googleapis.com https://fonts.gstatic.com; object-src 'none';"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response

    return app
