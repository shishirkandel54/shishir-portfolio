from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models import Page, Contact, Analytics, SiteConfig, Portfolio, Skill, CareerPath
from forms import ContactForm
from utils import track_page_view, get_client_ip
# from app import db
from extensions import db
import logging

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page"""
    # Track page view
    track_page_view(request)
    
    # Get featured pages
    featured_pages = Page.query.filter_by(is_published=True, is_featured=True).limit(3).all()
    
    # Get portfolio items for display
    portfolio_items = Portfolio.query.order_by(Portfolio.order_index.asc(), Portfolio.created_at.desc()).limit(9).all()
    
    # Get skills by category
    skills = Skill.query.filter_by(is_active=True).order_by(Skill.category.asc(), Skill.order_index.asc()).all()
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    # Get active career paths
    career_paths = CareerPath.query.filter_by(is_active=True).order_by(CareerPath.order_index.asc()).all()
    
    # Get site configuration
    site_config = {
        'site_title': SiteConfig.get_config('site_title', 'Shishir Kandel - Creative Graphic Designer'),
        'site_description': SiteConfig.get_config('site_description', 'Creative Graphic Designer crafting exceptional visual experiences'),
        'social_twitter': SiteConfig.get_config('social_twitter', '#'),
        'social_linkedin': SiteConfig.get_config('social_linkedin', 'https://www.linkedin.com/in/shishirkandel/'),
        'social_github': SiteConfig.get_config('social_github', 'https://github.com/shishirkandel'),
        'social_instagram': SiteConfig.get_config('social_instagram', 'https://www.instagram.com/the_shishir.kandel/'),
        'social_facebook': SiteConfig.get_config('social_facebook', 'https://www.facebook.com/shishir.kandel.772476'),
        'social_behance': SiteConfig.get_config('social_behance', 'https://www.behance.net/theshishirkandel'),
    }
    
    return render_template('index.html', 
                         featured_pages=featured_pages, 
                         config=site_config,
                         portfolio_items=portfolio_items,
                         skills_by_category=skills_by_category,
                         career_paths=career_paths)

@main_bp.route('/page/<slug>')
def page(slug):
    """Dynamic page display"""
    page = Page.query.filter_by(slug=slug, is_published=True).first_or_404()
    
    # Track page view
    track_page_view(request, page_title=page.title)
    
    return render_template(page.template_name, page=page)

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact form handling"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Create contact entry
        contact = Contact(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data,
            phone=form.phone.data,
            company=form.company.data,
            ip_address=get_client_ip(request),
            user_agent=request.headers.get('User-Agent', '')
        )
        
        try:
            db.session.add(contact)
            db.session.commit()
            flash('Thank you for your message! We will get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving contact form: {e}")
            flash('Sorry, there was an error sending your message. Please try again.', 'error')
    
    # Track page view
    track_page_view(request, page_title='Contact')
    
    return render_template('index.html', form=form, show_contact=True)

@main_bp.route('/api/contact', methods=['POST'])
def api_contact():
    """API endpoint for contact form (AJAX submission)"""
    if request.is_json:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field.title()} is required'}), 400
        
        # Create contact entry
        contact = Contact(
            name=data['name'][:100],
            email=data['email'][:120],
            subject=data.get('subject', '')[:200],
            message=data['message'][:2000],
            phone=data.get('phone', '')[:20],
            company=data.get('company', '')[:100],
            ip_address=get_client_ip(request),
            user_agent=request.headers.get('User-Agent', '')
        )
        
        try:
            db.session.add(contact)
            db.session.commit()
            return jsonify({'success': True, 'message': 'Thank you for your message!'})
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error saving contact form via API: {e}")
            return jsonify({'success': False, 'error': 'Database error'}), 500
    
    return jsonify({'success': False, 'error': 'Invalid request format'}), 400

@main_bp.route('/pages')
def pages():
    """List all published pages"""
    pages = Page.query.filter_by(is_published=True).order_by(Page.created_at.desc()).all()
    
    # Track page view
    track_page_view(request, page_title='Pages')
    
    return render_template('pages.html', pages=pages)

@main_bp.errorhandler(404)
def not_found_error(error):
    """404 error handler"""
    return render_template('404.html'), 404

@main_bp.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    return render_template('500.html'), 500
