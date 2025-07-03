#!/usr/bin/env python3
"""
Complete portfolio reset with correct order
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Portfolio

def reset_portfolio():
    with app.app_context():
        print("Resetting portfolio completely...")
        
        # Delete ALL portfolio items
        Portfolio.query.delete()
        db.session.commit()
        print("✓ Cleared all portfolio items")
        
        # Create portfolio items in correct order
        portfolio_items = [
            {
                'title': 'Latvia Embassy Appointment',
                'description': 'Professional appointment design for Latvia Embassy services with diplomatic aesthetics and clear information layout.',
                'image_url': '/static/uploads/latvia-embassy-appointment.jpg',
                'category': 'service-design',
                'tags': 'embassy, appointment, latvia, visa, professional, diplomatic',
                'is_featured': True,
                'order_index': 1
            },
            {
                'title': 'Nag Panchami Festival',
                'description': 'Traditional Nepali festival design celebrating Nag Panchami with Lord Shiva and sacred serpent imagery for E-Service Nepal.',
                'image_url': '/static/uploads/nag-panchami-festival.jpg',
                'category': 'cultural-design',
                'tags': 'festival, nag panchami, nepal, tradition, religious, shiva, cultural',
                'is_featured': True,
                'order_index': 2
            },
            {
                'title': 'Study in Newzealand',
                'description': 'Creative festival celebration cards featuring traditional Dashain elements and modern design aesthetics.',
                'image_url': '/static/uploads/kiec-study-newzealand.jpg',
                'category': 'cultural-design',
                'tags': 'Study, internation, newzealand',
                'is_featured': True,
                'order_index': 3
            },
            {
                'title': 'VFS Global Appointment',
                'description': 'Professional appointment booking design for VFS Global visa services with modern UI elements.',
                'image_url': '/static/uploads/vfs-global-appointment.jpg',
                'category': 'service-design',
                'tags': 'visa, appointment, service, professional, UI',
                'is_featured': False,
                'order_index': 4
            },
            {
                'title': 'Dr Cycle Store Social Media',
                'description': 'Dynamic social media promotional design for Dr Cycle Store featuring adventure and cycling themes.',
                'image_url': '/static/uploads/dr-cycle-store-promotion.jpg',
                'category': 'social-media',
                'tags': 'social media, cycling, sports, promotion, adventure',
                'is_featured': False,
                'order_index': 5
            },
            {
                'title': 'IMS Software Company',
                'description': 'Corporate branding design for IMS Software Company with modern technology aesthetics.',
                'image_url': '/static/uploads/ims-software-company.jpg',
                'category': 'corporate-design',
                'tags': 'corporate, software, branding, technology, business',
                'is_featured': False,
                'order_index': 6
            },
            {
                'title': 'Study in Canada - Expert Education',
                'description': 'Professional educational promotion design for Expert Education Canada study programs.',
                'image_url': '/static/uploads/study-canada-expert.jpg',
                'category': 'educational-design',
                'tags': 'education, canada, study abroad, visa, expert education',
                'is_featured': False,
                'order_index': 7
            },
            {
                'title': 'Study in Australia - KIEC',
                'description': 'Educational promotion design for Australian study programs through KIEC.',
                'image_url': '/static/uploads/kiec-study-australia.jpg',
                'category': 'educational-design',
                'tags': 'education, australia, study abroad, kiec, university',
                'is_featured': False,
                'order_index': 8
            },
            {
                'title': 'Study in South Korea',
                'description': 'Educational promotion for South Korean university programs with cultural elements.',
                'image_url': '/static/uploads/golden-eminent-south-korea.jpg',
                'category': 'educational-design',
                'tags': 'education, south korea, university, study abroad, cultural',
                'is_featured': False,
                'order_index': 9
            }
        ]
        
        # Add all portfolio items
        for item_data in portfolio_items:
            portfolio_item = Portfolio(**item_data)
            db.session.add(portfolio_item)
            print(f"✓ Added: {item_data['title']} (position {item_data['order_index']})")
        
        # Commit all changes
        db.session.commit()
        print("\n🎉 Portfolio reset complete!")
        print("📊 Nag Panchami is now in position 2")
        
        # Verify the final order
        print("\nFinal portfolio order:")
        portfolios = Portfolio.query.order_by(Portfolio.order_index.asc()).all()
        for i, portfolio in enumerate(portfolios):
            status = "✅ FEATURED" if portfolio.is_featured else "📌 Regular"
            print(f"{i+1}. {portfolio.title} - {status}")

if __name__ == '__main__':
    reset_portfolio()