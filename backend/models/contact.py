from datetime import datetime
from app import db

class Contact(db.Model):
    """Contact form submission model"""
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

    def __repr__(self):
        return f'<Contact {self.name} - {self.email}>'

    def mark_as_read(self):
        """Mark contact message as read"""
        self.is_read = True
        db.session.commit()