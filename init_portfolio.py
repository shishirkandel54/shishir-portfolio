#!/usr/bin/env python3
"""
Initialize portfolio with correct data and remove Expert Education entry
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Portfolio

def init_portfolio():
    with app.app_context():
        # Remove Expert Education entry
        expert_education = Portfolio.query.filter_by(title='Expert Education IELTS').first()
        if expert_education:
            db.session.delete(expert_education)
            print("Removed Expert Education entry")
        
        # Update Study in Canada entry
        study_canada = Portfolio.query.filter_by(title='Study in Canada').first()
        if study_canada:
            study_canada.image_url = '/static/uploads/study-canada-expert.jpg'
            study_canada.description = 'Professional educational promotion design for Expert Education Canada study programs'
            print("Updated Study in Canada entry")
        else:
            # Create new Study in Canada entry
            study_canada = Portfolio(
                title='Study in Canada - Expert Education',
                description='Professional educational promotion design for Expert Education Canada study programs',
                image_url='/static/uploads/study-canada-expert.jpg',
                category='educational-design',
                tags='education, canada, study abroad, visa, branding',
                is_featured=True,
                order_index=2
            )
            db.session.add(study_canada)
            print("Created Study in Canada entry")
        
        # Check if we need to add more portfolio items
        portfolio_items = [
            {
                'title': 'VFS Global Appointment',
                'description': 'Professional appointment booking design for VFS Global visa services',
                'image_url': '/static/uploads/vfs-global-appointment.jpg',
                'category': 'service-design',
                'tags': 'visa, appointment, service, professional',
                'is_featured': True,
                'order_index': 1
            },
            {
                'title': 'Dental Clinic Promotion',
                'description': 'Creative dental clinic promotional poster design',
                'image_url': '/static/uploads/chitwan-dental-poster.jpg',
                'category': 'healthcare-design',
                'tags': 'healthcare, dental, clinic, poster',
                'is_featured': False,
                'order_index': 3
            },
            {
                'title': 'Dr Cycle Store Social Media',
                'description': 'Social media promotional design for Dr Cycle Store',
                'image_url': '/static/uploads/dr-cycle-store-promotion.jpg',
                'category': 'social-media',
                'tags': 'social media, cycling, sports, promotion',
                'is_featured': False,
                'order_index': 4
            },
            {
                'title': 'IMS Software Company',
                'description': 'Corporate branding design for IMS Software Company',
                'image_url': '/static/uploads/ims-software-company.jpg',
                'category': 'corporate-design',
                'tags': 'corporate, software, branding, technology',
                'is_featured': False,
                'order_index': 5
            },
            {
                'title': 'Study in Australia - KIEC',
                'description': 'Educational promotion design for Australian study programs',
                'image_url': '/static/uploads/kiec-study-australia.jpg',
                'category': 'educational-design',
                'tags': 'education, australia, study abroad, kiec',
                'is_featured': False,
                'order_index': 6
            },
            {
                'title': 'Study in South Korea',
                'description': 'Educational promotion for South Korean university programs',
                'image_url': '/static/uploads/golden-eminent-south-korea.jpg',
                'category': 'educational-design',
                'tags': 'education, south korea, university, study abroad',
                'is_featured': False,
                'order_index': 7
            },
            {
                'title': 'Study in New Zealand - KIEC',
                'description': 'Educational promotion design for New Zealand study programs',
                'image_url': '/static/uploads/kiec-study-newzealand.jpg',
                'category': 'educational-design',
                'tags': 'education, new zealand, study abroad, kiec',
                'is_featured': False,
                'order_index': 8
            },
            {
                'title': 'Latvia Embassy Appointment',
                'description': 'Professional appointment design for Latvia Embassy services',
                'image_url': '/static/uploads/latvia-embassy-appointment.jpg',
                'category': 'service-design',
                'tags': 'embassy, appointment, latvia, visa, professional',
                'is_featured': True,
                'order_index': 9
            },
            {
                'title': 'Education Consultancy',
                'description': 'Study in Canada',
                'image_url': '/static/uploads/study-canada-expert.jpg',
                'category': 'cultural-design',
                'tags': 'Study, Canada, internation student',
                'is_featured': True,
                'order_index': 10
            }
        ]
        
        # Add portfolio items if they don't exist
        for item_data in portfolio_items:
            existing = Portfolio.query.filter_by(title=item_data['title']).first()
            if not existing:
                portfolio_item = Portfolio(**item_data)
                db.session.add(portfolio_item)
                print(f"Added portfolio item: {item_data['title']}")
        
        db.session.commit()
        print("Portfolio initialization complete!")

if __name__ == '__main__':
    init_portfolio()