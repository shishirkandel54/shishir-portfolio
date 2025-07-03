import os
import logging
from flask import Flask
from extensions import db, login_manager, migrate, csrf
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def create_app():
    app = Flask(__name__)
    
    # Configuration
    from config import Config
    app.config.from_object(Config)
    
    # Set secret key
    app.secret_key = os.environ.get("SESSION_SECRET", app.config.get('SECRET_KEY', 'dev-secret-key'))
    
    # Proxy fix for production
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import Admin
        return Admin.query.get(int(user_id))
    
    # Initialize database
    def init_db():
        with app.app_context():
            # Import all models
            from models import Admin, Page, Contact, Analytics, SiteConfig, Portfolio, Skill, CareerPath
            
            # Create tables
            db.create_all()
            
            # Create default admin user if not exists
            if not Admin.query.first():
                admin = Admin(
                    username='admin',
                    email='admin@example.com'
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("Default admin created - username: admin, password: admin123")
    
    # Initialize database
    init_db()

    # Register blueprints (import after init_db to avoid circular import)
    from views import main_bp
    from admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    return app

# Create the app
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)