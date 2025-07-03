#!/usr/bin/env python3
"""
Directly fix the second portfolio image to show Nag Panchami
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Portfolio

def fix_second_image():
    with app.app_context():
        print("Checking current portfolio order...")
        
        # Get all portfolio items ordered by index
        portfolios = Portfolio.query.order_by(Portfolio.order_index.asc()).all()
        
        for i, portfolio in enumerate(portfolios):
            print(f"Position {i+1} (order_index: {portfolio.order_index}): {portfolio.title} - {portfolio.image_url}")
        
        print("\nFixing second position...")
        
        # Delete any item that might be in second position (order_index 2)
        second_items = Portfolio.query.filter_by(order_index=2).all()
        for item in second_items:
            print(f"Removing from position 2: {item.title}")
            db.session.delete(item)
        
        # Also remove any Nag Panchami items that might exist elsewhere
        existing_nag = Portfolio.query.filter(Portfolio.title.contains('Nag Panchami')).all()
        for item in existing_nag:
            print(f"Removing existing Nag Panchami: {item.title}")
            db.session.delete(item)
        
        # Create fresh Nag Panchami item for position 2
        nag_panchami = Portfolio(
            title='Nag Panchami Festival',
            description='Traditional Nepali festival design celebrating Nag Panchami with Lord Shiva and sacred serpent imagery for E-Service Nepal',
            image_url='/static/uploads/nag-panchami-festival.jpg',
            category='cultural-design',
            tags='festival, nag panchami, nepal, tradition, religious, shiva, cultural',
            is_featured=True,
            order_index=2
        )
        db.session.add(nag_panchami)
        
        # Commit changes
        db.session.commit()
        
        print("\n✓ Fixed! Nag Panchami is now in position 2")
        
        # Verify the fix
        print("\nNew portfolio order:")
        portfolios = Portfolio.query.order_by(Portfolio.order_index.asc()).all()
        for i, portfolio in enumerate(portfolios):
            print(f"Position {i+1}: {portfolio.title} - {portfolio.image_url}")

if __name__ == '__main__':
    fix_second_image()