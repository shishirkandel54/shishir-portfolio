from flask import request, session
from models import Analytics
from extensions import db
import uuid
import logging

def get_client_ip(request):
    """Get client IP address from request"""
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip

def track_page_view(request, page_title=None):
    """Track page view analytics"""
    try:
        # Generate session ID if not exists
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        analytics = Analytics(
            page_url=request.path,
            page_title=page_title or request.endpoint,
            ip_address=get_client_ip(request),
            user_agent=request.headers.get('User-Agent', ''),
            referer=request.headers.get('Referer', ''),
            session_id=session['session_id']
        )
        
        db.session.add(analytics)
        db.session.commit()
    except Exception as e:
        logging.error(f"Error tracking page view: {e}")
        db.session.rollback()

def generate_slug(title):
    """Generate URL-friendly slug from title"""
    import re
    # Convert to lowercase and replace spaces with hyphens
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug.strip('-')

def truncate_text(text, length=100):
    """Truncate text to specified length"""
    if not text:
        return ''
    return text[:length] + '...' if len(text) > length else text

def format_datetime(dt, format='%Y-%m-%d %H:%M'):
    """Format datetime for display"""
    if not dt:
        return ''
    return dt.strftime(format)
