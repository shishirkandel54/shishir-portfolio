#!/usr/bin/env python3
"""
Setup script to initialize the portfolio with correct data
"""
import os
import sys
import shutil
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Portfolio, Admin

def setup_portfolio():
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        
        # Create default admin if not exists
        if not Admin.query.first():
            admin = Admin(
                username='admin',
                email='admin@example.com'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Default admin created (username: admin, password: admin123)")
        
        # Remove Expert Education if it exists
        expert_education = Portfolio.query.filter(Portfolio.title.like('%Expert Education%')).first()
        if expert_education:
            db.session.delete(expert_education)
            print("✓ Removed Expert Education entry")
        
        # Copy portfolio images to static/uploads
        upload_dir = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        
        # Copy the new images we added
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'portfolio-overview.png')):
            print("✓ Portfolio overview image found")
        if os.path.exists(os.path.join(os.path.dirname(__file__), 'static', 'uploads', 'study-canada-expert.jpg')):
            print("✓ Study Canada image found")
        
        # Portfolio data
        portfolio_items = [
            {
                'title': 'VFS Global Appointment',
                'description': 'Professional appointment booking design for VFS Global visa services with modern UI elements and clear information hierarchy.',
                'image_url': '/static/uploads/vfs-global-appointment.jpg',
                'category': 'service-design',
                'tags': 'visa, appointment, service, professional, UI design',
                'is_featured': True,
                'order_index': 1
            },
            {
                'title': 'Study in Canada - Expert Education',
                'description': 'Professional educational promotion design for Expert Education Canada study programs featuring modern graphics and clear messaging.',
                'image_url': '/static/uploads/study-canada-expert.jpg',
                'category': 'educational-design',
                'tags': 'education, canada, study abroad, visa, branding',
                'is_featured': True,
                'order_index': 2
            },
            {
                'title': 'Dental Clinic Creative Poster',
                'description': 'Creative dental clinic promotional poster design with vibrant colors and professional medical imagery.',
                'image_url': '/static/uploads/chitwan-dental-poster.jpg',
                'category': 'healthcare-design',
                'tags': 'healthcare, dental, clinic, poster, medical',
                'is_featured': False,
                'order_index': 3
            },
            {
                'title': 'Dr Cycle Store Social Media',
                'description': 'Dynamic social media promotional design for Dr Cycle Store featuring sports equipment and adventure themes.',
                'image_url': '/static/uploads/dr-cycle-store-promotion.jpg',
                'category': 'social-media',
                'tags': 'social media, cycling, sports, promotion, adventure',
                'is_featured': False,
                'order_index': 4
            },
            {
                'title': 'IMS Software Company',
                'description': 'Corporate branding design for IMS Software Company with modern tech aesthetics and professional layout.',
                'image_url': '/static/uploads/ims-software-company.jpg',
                'category': 'corporate-design',
                'tags': 'corporate, software, branding, technology, business',
                'is_featured': False,
                'order_index': 5
            },
            {
                'title': 'Study in Australia - KIEC',
                'description': 'Educational promotion design for Australian study programs through KIEC with engaging visuals and clear call-to-action.',
                'image_url': '/static/uploads/kiec-study-australia.jpg',
                'category': 'educational-design',
                'tags': 'education, australia, study abroad, kiec, university',
                'is_featured': False,
                'order_index': 6
            },
            {
                'title': 'Study in South Korea',
                'description': 'Educational promotion for South Korean university programs with cultural elements and modern design approach.',
                'image_url': '/static/uploads/golden-eminent-south-korea.jpg',
                'category': 'educational-design',
                'tags': 'education, south korea, university, study abroad, cultural',
                'is_featured': False,
                'order_index': 7
            },
            {
                'title': 'Study in New Zealand - KIEC',
                'description': 'Educational promotion design for New Zealand study programs featuring natural landscapes and educational themes.',
                'image_url': '/static/uploads/kiec-study-newzealand.jpg',
                'category': 'educational-design',
                'tags': 'education, new zealand, study abroad, kiec, nature',
                'is_featured': False,
                'order_index': 8
            },
            {
                'title': 'Latvia Embassy Appointment',
                'description': 'Professional appointment design for Latvia Embassy services with diplomatic aesthetics and clear information layout.',
                'image_url': '/static/uploads/latvia-embassy-appointment.jpg',
                'category': 'service-design',
                'tags': 'embassy, appointment, latvia, visa, professional, diplomatic',
                'is_featured': True,
                'order_index': 9
            },
            {
                'title': 'Dashain Festival Design',
                'description': 'Traditional festival celebration design for Dashain featuring cultural elements and festive colors.',
                'image_url': '/static/uploads/kiec-study-newzealand.jpg',
                'category': 'cultural-design',
                'tags': 'festival, dashain, traditional, cultural, celebration, nepal',
                'is_featured': True,
                'order_index': 10
            }
        ]
        
        # Add or update portfolio items
        for item_data in portfolio_items:
            existing = Portfolio.query.filter_by(title=item_data['title']).first()
            if existing:
                # Update existing item
                for key, value in item_data.items():
                    setattr(existing, key, value)
                print(f"✓ Updated: {item_data['title']}")
            else:
                # Create new item
                portfolio_item = Portfolio(**item_data)
                db.session.add(portfolio_item)
                print(f"✓ Added: {item_data['title']}")
        
        # Commit all changes
        db.session.commit()
        print("\n🎉 Portfolio setup complete!")
        print("📊 Portfolio items ready for deployment")
        print("🔐 Admin login: username='admin', password='admin123'")

if __name__ == '__main__':
    setup_portfolio()