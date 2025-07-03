#!/usr/bin/env python3
"""
Fix the portfolio by replacing the second image with Nag Panchami festival
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Portfolio

def fix_portfolio():
    with app.app_context():
        print("Fixing portfolio images...")
        
        # Get all portfolio items ordered by index
        portfolios = Portfolio.query.order_by(Portfolio.order_index.asc()).all()
        
        # Find and remove the problematic second item (black image)
        if len(portfolios) >= 2:
            second_item = portfolios[1]  # Index 1 is the second item
            print(f"Removing problematic item: {second_item.title}")
            db.session.delete(second_item)
        
        # Create/update the Nag Panchami festival item as the second item
        nag_panchami = Portfolio.query.filter_by(title='Nag Panchami Festival').first()
        if nag_panchami:
            nag_panchami.order_index = 2
            nag_panchami.image_url = '/static/uploads/nag-panchami-festival.jpg'
            print("Updated existing Nag Panchami item")
        else:
            # Create new Nag Panchami item
            nag_panchami = Portfolio(
                title='Nag Panchami Festival',
                description='Traditional Nepali festival design celebrating Nag Panchami with Lord Shiva and sacred serpent imagery',
                image_url='/static/uploads/nag-panchami-festival.jpg',
                category='cultural-design',
                tags='festival, nag panchami, nepal, tradition, religious, shiva',
                is_featured=True,
                order_index=2
            )
            db.session.add(nag_panchami)
            print("Created new Nag Panchami festival item")
        
        # Reorder remaining items
        remaining_portfolios = Portfolio.query.filter(Portfolio.title != 'Nag Panchami Festival').order_by(Portfolio.order_index.asc()).all()
        
        order = 1
        for portfolio in remaining_portfolios:
            if order == 2:  # Skip order 2, reserved for Nag Panchami
                order = 3
            portfolio.order_index = order
            print(f"Reordered: {portfolio.title} -> position {order}")
            order += 1
        
        # Commit changes
        db.session.commit()
        print("✓ Portfolio fixed successfully!")
        print("✓ Nag Panchami festival is now the second item")
        print("✓ All images should display properly")

if __name__ == '__main__':
    fix_portfolio()