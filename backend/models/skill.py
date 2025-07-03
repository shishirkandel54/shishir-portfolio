from datetime import datetime
from app import db

class Skill(db.Model):
    """Skills model"""
    __tablename__ = 'skills'
    
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