#!/usr/bin/env python3
"""
Shishir Portfolio Website
Run script for local development
"""

import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app

if __name__ == '__main__':
    # Set environment variables for local development
    os.environ.setdefault('SESSION_SECRET', 'dev-secret-key-portfolio-2025')
    
    print("🚀 Starting Shishir Portfolio Website...")
    print("📱 Responsive design optimized for mobile, tablet, and desktop")
    print("🎨 Design images integrated with animations")
    print("🌐 Website: http://localhost:5000")
    print("📊 API Endpoints:")
    print("   - GET /api/portfolio (Portfolio projects)")
    print("   - GET /api/skills (Skills data)")  
    print("   - POST /api/contact (Contact form)")
    print()
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=True
    )