from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
# from app import db
from extensions import db

class Admin(UserMixin, db.Model):
    """Admin user model for authentication"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Admin {self.username}>'

class Page(db.Model):
    """Page model for dynamic content management"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text)
    meta_description = db.Column(db.Text)
    meta_keywords = db.Column(db.String(500))
    is_published = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    template_name = db.Column(db.String(100), default='page.html')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Page {self.title}>'
    
    @property
    def url(self):
        """Get the URL for this page"""
        return f'/page/{self.slug}'

class Contact(db.Model):
    """Contact form submission model"""
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
    
    def __repr__(self):
        return f'<Contact {self.name} - {self.email}>'
    
    def mark_as_read(self):
        """Mark contact message as read"""
        self.is_read = True
        db.session.commit()

class Analytics(db.Model):
    """Analytics tracking model"""
    id = db.Column(db.Integer, primary_key=True)
    page_url = db.Column(db.String(500), nullable=False)
    page_title = db.Column(db.String(200))
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    referer = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.String(100))
    
    def __repr__(self):
        return f'<Analytics {self.page_url} - {self.timestamp}>'

class SiteConfig(db.Model):
    """Site configuration model"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SiteConfig {self.key}>'
    
    @staticmethod
    def get_config(key, default=None):
        """Get configuration value by key"""
        config = SiteConfig.query.filter_by(key=key).first()
        return config.value if config else default
    
    @staticmethod
    def set_config(key, value, description=None):
        """Set configuration value"""
        config = SiteConfig.query.filter_by(key=key).first()
        if config:
            config.value = value
            config.updated_at = datetime.utcnow()
        else:
            config = SiteConfig(key=key, value=value, description=description)
            db.session.add(config)
        db.session.commit()
        return config

class Portfolio(db.Model):
    """Portfolio project model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    project_url = db.Column(db.String(500))
    category = db.Column(db.String(100))
    tags = db.Column(db.String(500))  # Comma-separated tags
    is_featured = db.Column(db.Boolean, default=False)
    order_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Portfolio {self.title}>'
    
    @property
    def tag_list(self):
        """Get tags as a list"""
        return [tag.strip() for tag in self.tags.split(',')] if self.tags else []

class Skill(db.Model):
    """Skills model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)  # Design Software, Specializations, Additional Skills
    icon_class = db.Column(db.String(100))  # Font Awesome class
    color = db.Column(db.String(20), default='#8b5cf6')
    proficiency = db.Column(db.Integer, default=80)  # 0-100
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Skill {self.name}>'

class CareerPath(db.Model):
    """Career paths model"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    icon_class = db.Column(db.String(100))
    icon_color = db.Column(db.String(100))
    skills = db.Column(db.Text)  # Comma-separated skills
    salary_range = db.Column(db.String(100))
    learning_time = db.Column(db.String(100))
    order_index = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CareerPath {self.title}>'
    
    @property
    def skill_list(self):
        """Get skills as a list"""
        return [skill.strip() for skill in self.skills.split(',')] if self.skills else []
