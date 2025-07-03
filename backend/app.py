import os
from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app():
    app = Flask(__name__, 
                template_folder='../frontend/templates',
                static_folder='../frontend/static')
    
    # Configure app
    app.secret_key = os.environ.get('SESSION_SECRET', 'dev-secret-key-change-in-production')
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Database configuration
    if os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    else:
        # Local SQLite database for development
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
    
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    csrf = CSRFProtect(app)
    CORS(app, origins=['http://localhost:5000'])  # Enable CORS for API requests
    
    # Configure uploads
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'static', 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Import models (they need to be defined in the same file for now)
    class Portfolio(db.Model):
        __tablename__ = 'portfolio'
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        description = db.Column(db.Text)
        image_url = db.Column(db.String(500))
        project_url = db.Column(db.String(500))
        category = db.Column(db.String(100))
        tags = db.Column(db.String(500))
        is_featured = db.Column(db.Boolean, default=False)
        is_active = db.Column(db.Boolean, default=True)
        order_index = db.Column(db.Integer, default=0)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        def tag_list(self):
            if self.tags:
                return [tag.strip() for tag in self.tags.split(',')]
            return []
    
    class Contact(db.Model):
        __tablename__ = 'contact'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(120), nullable=False)
        subject = db.Column(db.String(200))
        message = db.Column(db.Text, nullable=False)
        phone = db.Column(db.String(20))
        company = db.Column(db.String(100))
        is_read = db.Column(db.Boolean, default=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        ip_address = db.Column(db.String(45))
        user_agent = db.Column(db.String(500))
    
    class Skill(db.Model):
        __tablename__ = 'skills'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        category = db.Column(db.String(100), nullable=False)
        icon_class = db.Column(db.String(100))
        color = db.Column(db.String(20), default='#8b5cf6')
        proficiency = db.Column(db.Integer, default=80)
        order_index = db.Column(db.Integer, default=0)
        is_active = db.Column(db.Boolean, default=True)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    class Admin(db.Model):
        __tablename__ = 'admin'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(256), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        last_login = db.Column(db.DateTime)
        active = db.Column(db.Boolean, default=True)
        
        def check_password(self, password):
            from werkzeug.security import check_password_hash
            return check_password_hash(self.password_hash, password)
        
        def set_password(self, password):
            from werkzeug.security import generate_password_hash
            self.password_hash = generate_password_hash(password)
    
    class SiteConfig(db.Model):
        __tablename__ = 'site_config'
        id = db.Column(db.Integer, primary_key=True)
        key = db.Column(db.String(100), unique=True, nullable=False)
        value = db.Column(db.Text)
        description = db.Column(db.String(500))
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Create sample data if none exists
        if not Portfolio.query.first():
            sample_projects = [
                Portfolio(
                    title="Creative Design Suite",
                    description="A comprehensive design project showcasing modern UI/UX principles with interactive animations.",
                    image_url="/static/images/design-tools.png",
                    category="UI/UX Design",
                    tags="Design, Animation, Creative",
                    is_featured=True
                ),
                Portfolio(
                    title="Brand Identity Package", 
                    description="Complete branding solution with logo design, color palette, and visual guidelines.",
                    image_url="/static/images/figma-icon.png",
                    category="Branding",
                    tags="Branding, Logo, Identity",
                    is_featured=True
                ),
                Portfolio(
                    title="Interactive Web Experience",
                    description="Modern web design with smooth animations and responsive layouts.",
                    image_url="/static/images/creative-blob.png", 
                    category="Web Design",
                    tags="Web, Interactive, Animation",
                    is_featured=False
                )
            ]
            
            for project in sample_projects:
                db.session.add(project)
                
            # Add sample skills
            sample_skills = [
                Skill(name="Adobe Photoshop", category="Design Software", proficiency=95),
                Skill(name="Adobe Illustrator", category="Design Software", proficiency=90),
                Skill(name="Figma", category="Design Software", proficiency=85),
                Skill(name="UI/UX Design", category="Design Specializations", proficiency=90),
                Skill(name="Brand Identity", category="Design Specializations", proficiency=85),
                Skill(name="Web Design", category="Design Specializations", proficiency=80)
            ]
            
            for skill in sample_skills:
                db.session.add(skill)
                
            db.session.commit()
            app.logger.info("Sample data created successfully")
            
        # Create default admin user if none exists
        if not Admin.query.first():
            admin = Admin(username='admin', email='admin@shishir.design')
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Add default site configuration
            default_configs = [
                ('site_title', 'Shishir - Creative Designer', 'Website title'),
                ('site_description', 'Professional creative designer specializing in UI/UX and brand identity', 'Website description'),
                ('contact_email', 'hello@shishir.design', 'Contact email address'),
                ('contact_phone', '+1 (555) 123-4567', 'Contact phone number'),
                ('hero_title', 'Creative Designer', 'Homepage hero title'),
                ('hero_subtitle', 'Transforming ideas into stunning visual experiences', 'Homepage hero subtitle'),
                ('social_linkedin', '#', 'LinkedIn profile URL'),
                ('social_behance', '#', 'Behance profile URL'),
                ('social_dribbble', '#', 'Dribbble profile URL'),
                ('social_instagram', '#', 'Instagram profile URL')
            ]
            
            for key, value, description in default_configs:
                config = SiteConfig(key=key, value=value, description=description)
                db.session.add(config)
            
            db.session.commit()
            app.logger.info("Default admin user and site config created")
    
    # Register API routes
    @app.route('/api/portfolio', methods=['GET'])
    def get_portfolio():
        """Get all portfolio projects"""
        projects = Portfolio.query.filter_by(is_active=True).order_by(Portfolio.order_index).all()
        return jsonify([{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'image_url': p.image_url,
            'project_url': p.project_url,
            'category': p.category,
            'tags': p.tag_list(),
            'is_featured': p.is_featured,
            'created_at': p.created_at.isoformat() if p.created_at else None
        } for p in projects])
    
    @app.route('/api/skills', methods=['GET'])
    def get_skills():
        """Get all skills grouped by category"""
        skills = Skill.query.filter_by(is_active=True).order_by(Skill.category, Skill.order_index).all()
        skills_by_category = {}
        
        for skill in skills:
            if skill.category not in skills_by_category:
                skills_by_category[skill.category] = []
            skills_by_category[skill.category].append({
                'id': skill.id,
                'name': skill.name,
                'proficiency': skill.proficiency,
                'icon_class': skill.icon_class,
                'color': skill.color
            })
        
        return jsonify(skills_by_category)
    
    @app.route('/api/contact', methods=['POST'])
    def submit_contact():
        """Handle contact form submission"""
        try:
            data = request.get_json()
            
            contact = Contact(
                name=data.get('name'),
                email=data.get('email'),
                subject=data.get('subject', ''),
                message=data.get('message'),
                phone=data.get('phone', ''),
                company=data.get('company', ''),
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')
            )
            
            db.session.add(contact)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Thank you for your message! I will get back to you soon.'
            })
            
        except Exception as e:
            app.logger.error(f"Contact form error: {e}")
            return jsonify({
                'success': False,
                'message': 'Sorry, there was an error sending your message. Please try again.'
            }), 500
    
    # ========================================================================
    # ADMIN AUTHENTICATION
    # ========================================================================
    
    def require_auth():
        """Check if user is authenticated"""
        return session.get('admin_logged_in') == True
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        """Admin login"""
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            admin = Admin.query.filter_by(username=username).first()
            
            if admin and admin.check_password(password) and admin.active:
                session['admin_logged_in'] = True
                session['admin_id'] = admin.id
                admin.last_login = datetime.utcnow()
                db.session.commit()
                flash('Welcome to the admin panel!', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('Invalid username or password', 'error')
        
        return render_template('admin/login.html')
    
    @app.route('/admin/logout')
    def admin_logout():
        """Admin logout"""
        session.clear()
        flash('You have been logged out', 'info')
        return redirect(url_for('admin_login'))
    
    # ========================================================================
    # ADMIN DASHBOARD
    # ========================================================================
    
    @app.route('/admin')
    @app.route('/admin/dashboard')
    def admin_dashboard():
        """Admin dashboard"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        # Get statistics
        stats = {
            'total_projects': Portfolio.query.count(),
            'featured_projects': Portfolio.query.filter_by(is_featured=True).count(),
            'total_skills': Skill.query.filter_by(is_active=True).count(),
            'total_contacts': Contact.query.count(),
            'unread_contacts': Contact.query.filter_by(is_read=False).count(),
            'recent_contacts': Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
        }
        
        return render_template('admin/dashboard.html', stats=stats)
    
    # ========================================================================
    # PORTFOLIO MANAGEMENT
    # ========================================================================
    
    @app.route('/admin/portfolio')
    def admin_portfolio():
        """Portfolio management"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        projects = Portfolio.query.order_by(Portfolio.order_index, Portfolio.created_at.desc()).all()
        return render_template('admin/portfolio.html', projects=projects)
    
    @app.route('/admin/portfolio/new', methods=['GET', 'POST'])
    def admin_portfolio_new():
        """Create new portfolio project"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        if request.method == 'POST':
            # Handle file upload
            image_url = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_url = f'/static/uploads/{filename}'
            
            project = Portfolio(
                title=request.form.get('title'),
                description=request.form.get('description'),
                image_url=image_url or request.form.get('image_url'),
                project_url=request.form.get('project_url'),
                category=request.form.get('category'),
                tags=request.form.get('tags'),
                is_featured=bool(request.form.get('is_featured')),
                order_index=int(request.form.get('order_index', 0))
            )
            
            db.session.add(project)
            db.session.commit()
            flash('Portfolio project created successfully!', 'success')
            return redirect(url_for('admin_portfolio'))
        
        return render_template('admin/portfolio_form.html', project=None)
    
    @app.route('/admin/portfolio/<int:project_id>/edit', methods=['GET', 'POST'])
    def admin_portfolio_edit(project_id):
        """Edit portfolio project"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        project = Portfolio.query.get_or_404(project_id)
        
        if request.method == 'POST':
            # Handle file upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    project.image_url = f'/static/uploads/{filename}'
            elif request.form.get('image_url'):
                project.image_url = request.form.get('image_url')
            
            project.title = request.form.get('title')
            project.description = request.form.get('description')
            project.project_url = request.form.get('project_url')
            project.category = request.form.get('category')
            project.tags = request.form.get('tags')
            project.is_featured = bool(request.form.get('is_featured'))
            project.order_index = int(request.form.get('order_index', 0))
            
            db.session.commit()
            flash('Portfolio project updated successfully!', 'success')
            return redirect(url_for('admin_portfolio'))
        
        return render_template('admin/portfolio_form.html', project=project)
    
    @app.route('/admin/portfolio/<int:project_id>/delete', methods=['POST'])
    def admin_portfolio_delete(project_id):
        """Delete portfolio project"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        project = Portfolio.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        flash('Portfolio project deleted successfully!', 'success')
        return redirect(url_for('admin_portfolio'))
    
    # ========================================================================
    # CONTACT MANAGEMENT
    # ========================================================================
    
    @app.route('/admin/contacts')
    def admin_contacts():
        """Contact management"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return render_template('admin/contacts.html', contacts=contacts)
    
    @app.route('/admin/contacts/<int:contact_id>/toggle-read', methods=['POST'])
    def admin_contact_toggle_read(contact_id):
        """Toggle contact read status"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        contact = Contact.query.get_or_404(contact_id)
        contact.is_read = not contact.is_read
        db.session.commit()
        
        status = 'read' if contact.is_read else 'unread'
        flash(f'Contact marked as {status}!', 'success')
        return redirect(url_for('admin_contacts'))
    
    @app.route('/admin/contacts/<int:contact_id>/delete', methods=['POST'])
    def admin_contact_delete(contact_id):
        """Delete contact"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        flash('Contact deleted successfully!', 'success')
        return redirect(url_for('admin_contacts'))
    
    # ========================================================================
    # SKILLS MANAGEMENT
    # ========================================================================
    
    @app.route('/admin/skills')
    def admin_skills():
        """Skills management"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        skills = Skill.query.order_by(Skill.category, Skill.order_index).all()
        return render_template('admin/skills.html', skills=skills)
    
    @app.route('/admin/skills/new', methods=['GET', 'POST'])
    def admin_skills_new():
        """Create new skill"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        if request.method == 'POST':
            skill = Skill(
                name=request.form.get('name'),
                category=request.form.get('category'),
                icon_class=request.form.get('icon_class'),
                color=request.form.get('color', '#8b5cf6'),
                proficiency=int(request.form.get('proficiency', 80)),
                order_index=int(request.form.get('order_index', 0)),
                is_active=bool(request.form.get('is_active', True))
            )
            
            db.session.add(skill)
            db.session.commit()
            flash('Skill created successfully!', 'success')
            return redirect(url_for('admin_skills'))
        
        return render_template('admin/skills_form.html', skill=None)
    
    @app.route('/admin/skills/<int:skill_id>/edit', methods=['GET', 'POST'])
    def admin_skills_edit(skill_id):
        """Edit skill"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        skill = Skill.query.get_or_404(skill_id)
        
        if request.method == 'POST':
            skill.name = request.form.get('name')
            skill.category = request.form.get('category')
            skill.icon_class = request.form.get('icon_class')
            skill.color = request.form.get('color', '#8b5cf6')
            skill.proficiency = int(request.form.get('proficiency', 80))
            skill.order_index = int(request.form.get('order_index', 0))
            skill.is_active = bool(request.form.get('is_active'))
            
            db.session.commit()
            flash('Skill updated successfully!', 'success')
            return redirect(url_for('admin_skills'))
        
        return render_template('admin/skills_form.html', skill=skill)
    
    @app.route('/admin/skills/<int:skill_id>/delete', methods=['POST'])
    def admin_skills_delete(skill_id):
        """Delete skill"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        skill = Skill.query.get_or_404(skill_id)
        db.session.delete(skill)
        db.session.commit()
        flash('Skill deleted successfully!', 'success')
        return redirect(url_for('admin_skills'))
    
    # ========================================================================
    # SITE SETTINGS
    # ========================================================================
    
    @app.route('/admin/settings', methods=['GET', 'POST'])
    def admin_settings():
        """Site settings management"""
        if not require_auth():
            return redirect(url_for('admin_login'))
        
        if request.method == 'POST':
            # Update site configuration
            for key, value in request.form.items():
                if key != 'csrf_token':
                    config = SiteConfig.query.filter_by(key=key).first()
                    if config:
                        config.value = value
                        config.updated_at = datetime.utcnow()
                    else:
                        config = SiteConfig(key=key, value=value)
                        db.session.add(config)
            
            db.session.commit()
            flash('Settings updated successfully!', 'success')
            return redirect(url_for('admin_settings'))
        
        # Get all configuration
        configs = {config.key: config.value for config in SiteConfig.query.all()}
        return render_template('admin/settings.html', configs=configs)
    
    # Frontend routes
    @app.route('/')
    def index():
        """Homepage"""
        return render_template('index.html')
    
    @app.route('/portfolio')
    def portfolio():
        """Portfolio page"""
        return render_template('portfolio.html')
    
    @app.route('/contact')
    def contact():
        """Contact page"""
        return render_template('contact.html')
    
    @app.route('/static/<path:filename>')
    def static_files(filename):
        """Serve static files"""
        return send_from_directory(app.static_folder, filename)
    
    return app

# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)