from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import Admin, Page, Contact, Analytics, SiteConfig, Portfolio, Skill, CareerPath
from forms import LoginForm, PageForm, SiteConfigForm, PortfolioForm, SkillForm, CareerPathForm
from utils import get_client_ip
# from app import db
from extensions import db
from datetime import datetime, timedelta
import logging

admin_bp = Blueprint('admin', __name__, template_folder='templates/admin')

@admin_bp.route('/')
@login_required
def dashboard():
    """Admin dashboard"""
    # Get statistics
    stats = {
        'total_pages': Page.query.count(),
        'published_pages': Page.query.filter_by(is_published=True).count(),
        'total_contacts': Contact.query.count(),
        'unread_contacts': Contact.query.filter_by(is_read=False).count(),
        'page_views_today': Analytics.query.filter(
            Analytics.timestamp >= datetime.utcnow().date()
        ).count(),
        'page_views_week': Analytics.query.filter(
            Analytics.timestamp >= datetime.utcnow() - timedelta(days=7)
        ).count(),
    }
    
    # Recent contacts
    recent_contacts = Contact.query.order_by(Contact.created_at.desc()).limit(5).all()
    
    # Recent page views
    recent_views = Analytics.query.order_by(Analytics.timestamp.desc()).limit(10).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_contacts=recent_contacts,
                         recent_views=recent_views)

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        
        if admin and admin.check_password(form.password.data):
            # Update last login
            admin.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(admin, remember=form.remember_me.data)
            flash('Login successful!', 'success')
            
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))

@admin_bp.route('/pages')
@login_required
def pages():
    """Pages management"""
    page_num = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Page.query
    if search:
        query = query.filter(Page.title.contains(search) | Page.content.contains(search))
    
    pages = query.order_by(Page.updated_at.desc()).paginate(
        page=page_num, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False
    )
    
    return render_template('admin/pages.html', pages=pages, search=search)

@admin_bp.route('/pages/new', methods=['GET', 'POST'])
@login_required
def new_page():
    """Create new page"""
    form = PageForm()
    
    if form.validate_on_submit():
        # Check if slug exists
        existing_page = Page.query.filter_by(slug=form.slug.data).first()
        if existing_page:
            flash('A page with this slug already exists', 'error')
            return render_template('admin/page_form.html', form=form, title='New Page')
        
        page = Page(
            title=form.title.data,
            slug=form.slug.data,
            content=form.content.data,
            meta_description=form.meta_description.data,
            meta_keywords=form.meta_keywords.data,
            template_name=form.template_name.data,
            is_published=form.is_published.data,
            is_featured=form.is_featured.data
        )
        
        try:
            db.session.add(page)
            db.session.commit()
            flash('Page created successfully!', 'success')
            return redirect(url_for('admin.pages'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error creating page: {e}")
            flash('Error creating page', 'error')
    
    return render_template('admin/page_form.html', form=form, title='New Page')

@admin_bp.route('/pages/<int:page_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_page(page_id):
    """Edit existing page"""
    page = Page.query.get_or_404(page_id)
    form = PageForm(obj=page)
    
    if form.validate_on_submit():
        # Check if slug exists (excluding current page)
        existing_page = Page.query.filter(Page.slug == form.slug.data, Page.id != page_id).first()
        if existing_page:
            flash('A page with this slug already exists', 'error')
            return render_template('admin/page_form.html', form=form, title='Edit Page', page=page)
        
        page.title = form.title.data
        page.slug = form.slug.data
        page.content = form.content.data
        page.meta_description = form.meta_description.data
        page.meta_keywords = form.meta_keywords.data
        page.template_name = form.template_name.data
        page.is_published = form.is_published.data
        page.is_featured = form.is_featured.data
        page.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Page updated successfully!', 'success')
            return redirect(url_for('admin.pages'))
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error updating page: {e}")
            flash('Error updating page', 'error')
    
    return render_template('admin/page_form.html', form=form, title='Edit Page', page=page)

@admin_bp.route('/pages/<int:page_id>/delete', methods=['POST'])
@login_required
def delete_page(page_id):
    """Delete page"""
    page = Page.query.get_or_404(page_id)
    
    try:
        db.session.delete(page)
        db.session.commit()
        flash('Page deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting page: {e}")
        flash('Error deleting page', 'error')
    
    return redirect(url_for('admin.pages'))

@admin_bp.route('/contacts')
@login_required
def contacts():
    """Contact messages management"""
    page_num = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    filter_read = request.args.get('read', '')
    
    query = Contact.query
    if search:
        query = query.filter(
            Contact.name.contains(search) | 
            Contact.email.contains(search) | 
            Contact.subject.contains(search) |
            Contact.message.contains(search)
        )
    
    if filter_read == 'unread':
        query = query.filter_by(is_read=False)
    elif filter_read == 'read':
        query = query.filter_by(is_read=True)
    
    contacts = query.order_by(Contact.created_at.desc()).paginate(
        page=page_num, per_page=current_app.config['ITEMS_PER_PAGE'], error_out=False
    )
    
    return render_template('admin/contacts.html', 
                         contacts=contacts, 
                         search=search, 
                         filter_read=filter_read)

@admin_bp.route('/contacts/<int:contact_id>/mark-read', methods=['POST'])
@login_required
def mark_contact_read(contact_id):
    """Mark contact as read"""
    contact = Contact.query.get_or_404(contact_id)
    contact.mark_as_read()
    flash('Contact marked as read', 'success')
    return redirect(url_for('admin.contacts'))

@admin_bp.route('/contacts/<int:contact_id>/delete', methods=['POST'])
@login_required
def delete_contact(contact_id):
    """Delete contact message"""
    contact = Contact.query.get_or_404(contact_id)
    
    try:
        db.session.delete(contact)
        db.session.commit()
        flash('Contact message deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        logging.error(f"Error deleting contact: {e}")
        flash('Error deleting contact message', 'error')
    
    return redirect(url_for('admin.contacts'))

@admin_bp.route('/analytics')
@login_required
def analytics():
    """Analytics dashboard"""
    # Date range
    days = request.args.get('days', 7, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    # Page views by day
    daily_views = db.session.query(
        db.func.date(Analytics.timestamp).label('date'),
        db.func.count(Analytics.id).label('views')
    ).filter(Analytics.timestamp >= start_date).group_by(
        db.func.date(Analytics.timestamp)
    ).order_by(db.func.date(Analytics.timestamp)).all()
    
    # Top pages
    top_pages = db.session.query(
        Analytics.page_url,
        Analytics.page_title,
        db.func.count(Analytics.id).label('views')
    ).filter(Analytics.timestamp >= start_date).group_by(
        Analytics.page_url, Analytics.page_title
    ).order_by(db.func.count(Analytics.id).desc()).limit(10).all()
    
    # Total stats
    total_views = Analytics.query.filter(Analytics.timestamp >= start_date).count()
    unique_visitors = db.session.query(
        db.func.count(db.func.distinct(Analytics.ip_address))
    ).filter(Analytics.timestamp >= start_date).scalar()
    
    stats = {
        'total_views': total_views,
        'unique_visitors': unique_visitors,
        'daily_views': daily_views,
        'top_pages': top_pages,
        'days': days
    }
    
    return render_template('admin/analytics.html', stats=stats)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """Site settings"""
    form = SiteConfigForm()
    
    if form.validate_on_submit():
        # Save configuration
        SiteConfig.set_config('site_title', form.site_title.data, 'Site title')
        SiteConfig.set_config('site_description', form.site_description.data, 'Site description')
        SiteConfig.set_config('contact_email', form.contact_email.data, 'Contact email')
        SiteConfig.set_config('contact_phone', form.contact_phone.data, 'Contact phone')
        SiteConfig.set_config('contact_location', form.contact_location.data, 'Contact location')
        SiteConfig.set_config('hero_title', form.hero_title.data, 'Hero section title')
        SiteConfig.set_config('hero_subtitle', form.hero_subtitle.data, 'Hero section subtitle')
        SiteConfig.set_config('about_title', form.about_title.data, 'About section title')
        SiteConfig.set_config('about_content', form.about_content.data, 'About section content')
        SiteConfig.set_config('social_twitter', form.social_twitter.data, 'Twitter URL')
        SiteConfig.set_config('social_linkedin', form.social_linkedin.data, 'LinkedIn URL')
        SiteConfig.set_config('social_github', form.social_github.data, 'GitHub URL')
        SiteConfig.set_config('social_instagram', form.social_instagram.data, 'Instagram URL')
        SiteConfig.set_config('social_facebook', form.social_facebook.data, 'Facebook URL')
        SiteConfig.set_config('social_behance', form.social_behance.data, 'Behance URL')
        
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('admin.settings'))
    
    # Load current configuration
    form.site_title.data = SiteConfig.get_config('site_title', 'Shishir Kandel - Creative Graphic Designer')
    form.site_description.data = SiteConfig.get_config('site_description', 'Creative Graphic Designer crafting exceptional visual experiences')
    form.contact_email.data = SiteConfig.get_config('contact_email', 'info.hubcreative@gmail.com')
    form.contact_phone.data = SiteConfig.get_config('contact_phone', '+977 9848000000')
    form.contact_location.data = SiteConfig.get_config('contact_location', 'Bharatpur, Nepal')
    form.hero_title.data = SiteConfig.get_config('hero_title', 'Hi, I\'m Shishir Kandel')
    form.hero_subtitle.data = SiteConfig.get_config('hero_subtitle', 'Creative Graphic Designer crafting exceptional visual experiences with modern design tools and creative solutions')
    form.about_title.data = SiteConfig.get_config('about_title', 'Creative Graphic Designer')
    form.about_content.data = SiteConfig.get_config('about_content', 'I\'m a passionate graphic designer with extensive experience in creating compelling visual content that communicates ideas effectively.')
    form.social_twitter.data = SiteConfig.get_config('social_twitter', '')
    form.social_linkedin.data = SiteConfig.get_config('social_linkedin', 'https://www.linkedin.com/in/shishirkandel/')
    form.social_github.data = SiteConfig.get_config('social_github', 'https://github.com/shishirkandel')
    form.social_instagram.data = SiteConfig.get_config('social_instagram', 'https://www.instagram.com/the_shishir.kandel/')
    form.social_facebook.data = SiteConfig.get_config('social_facebook', 'https://www.facebook.com/shishir.kandel.772476')
    form.social_behance.data = SiteConfig.get_config('social_behance', 'https://www.behance.net/theshishirkandel')
    
    return render_template('admin/settings.html', form=form)

# Portfolio Management Routes
@admin_bp.route('/portfolio')
@login_required
def portfolio():
    """Portfolio management"""
    page = request.args.get('page', 1, type=int)
    portfolios = Portfolio.query.order_by(Portfolio.order_index.asc(), Portfolio.created_at.desc()).paginate(
        page=page, per_page=12, error_out=False
    )
    return render_template('admin/portfolio.html', portfolios=portfolios)

@admin_bp.route('/portfolio/new', methods=['GET', 'POST'])
@login_required
def new_portfolio():
    """Create new portfolio project"""
    form = PortfolioForm()
    
    if form.validate_on_submit():
        # Handle file upload
        image_url = form.image_url.data
        if form.image_file.data:
            # Save uploaded file
            import os
            import uuid
            from werkzeug.utils import secure_filename
            
            file = form.image_file.data
            filename = secure_filename(file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Ensure upload directory exists
            upload_dir = os.path.join(current_app.static_folder, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_dir, unique_filename)
            file.save(file_path)
            image_url = f"/static/uploads/{unique_filename}"
        
        portfolio = Portfolio(
            title=form.title.data,
            description=form.description.data,
            image_url=image_url,
            project_url=form.project_url.data,
            category=form.category.data,
            tags=form.tags.data,
            is_featured=form.is_featured.data,
            order_index=form.order_index.data
        )
        db.session.add(portfolio)
        db.session.commit()
        
        flash(f'Portfolio project "{portfolio.title}" created successfully!', 'success')
        return redirect(url_for('admin.portfolio'))
    
    return render_template('admin/portfolio_form.html', form=form, title='New Portfolio Project')

@admin_bp.route('/portfolio/<int:portfolio_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_portfolio(portfolio_id):
    """Edit portfolio project"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    form = PortfolioForm(obj=portfolio)
    
    if form.validate_on_submit():
        portfolio.title = form.title.data
        portfolio.description = form.description.data
        portfolio.image_url = form.image_url.data
        portfolio.project_url = form.project_url.data
        portfolio.category = form.category.data
        portfolio.tags = form.tags.data
        portfolio.is_featured = form.is_featured.data
        portfolio.order_index = form.order_index.data
        portfolio.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash(f'Portfolio project "{portfolio.title}" updated successfully!', 'success')
        return redirect(url_for('admin.portfolio'))
    
    return render_template('admin/portfolio_form.html', form=form, portfolio=portfolio, title='Edit Portfolio Project')

@admin_bp.route('/portfolio/<int:portfolio_id>/delete', methods=['POST'])
@login_required
def delete_portfolio(portfolio_id):
    """Delete portfolio project"""
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    title = portfolio.title
    
    db.session.delete(portfolio)
    db.session.commit()
    
    flash(f'Portfolio project "{title}" deleted successfully!', 'success')
    return redirect(url_for('admin.portfolio'))

# Skills Management Routes
@admin_bp.route('/skills')
@login_required
def skills():
    """Skills management"""
    skills = Skill.query.order_by(Skill.category.asc(), Skill.order_index.asc()).all()
    skills_by_category = {}
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    return render_template('admin/skills.html', skills_by_category=skills_by_category)

@admin_bp.route('/skills/new', methods=['GET', 'POST'])
@login_required
def new_skill():
    """Create new skill"""
    form = SkillForm()
    
    if form.validate_on_submit():
        skill = Skill(
            name=form.name.data,
            category=form.category.data,
            icon_class=form.icon_class.data,
            color=form.color.data,
            proficiency=form.proficiency.data,
            order_index=form.order_index.data,
            is_active=form.is_active.data
        )
        db.session.add(skill)
        db.session.commit()
        
        flash(f'Skill "{skill.name}" created successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skill_form.html', form=form, title='New Skill')

@admin_bp.route('/skills/<int:skill_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_skill(skill_id):
    """Edit skill"""
    skill = Skill.query.get_or_404(skill_id)
    form = SkillForm(obj=skill)
    
    if form.validate_on_submit():
        skill.name = form.name.data
        skill.category = form.category.data
        skill.icon_class = form.icon_class.data
        skill.color = form.color.data
        skill.proficiency = form.proficiency.data
        skill.order_index = form.order_index.data
        skill.is_active = form.is_active.data
        
        db.session.commit()
        flash(f'Skill "{skill.name}" updated successfully!', 'success')
        return redirect(url_for('admin.skills'))
    
    return render_template('admin/skill_form.html', form=form, skill=skill, title='Edit Skill')

@admin_bp.route('/skills/<int:skill_id>/delete', methods=['POST'])
@login_required
def delete_skill(skill_id):
    """Delete skill"""
    skill = Skill.query.get_or_404(skill_id)
    name = skill.name
    
    db.session.delete(skill)
    db.session.commit()
    
    flash(f'Skill "{name}" deleted successfully!', 'success')
    return redirect(url_for('admin.skills'))

# Career Paths Management Routes
@admin_bp.route('/careers')
@login_required
def careers():
    """Career paths management"""
    careers = CareerPath.query.order_by(CareerPath.order_index.asc(), CareerPath.created_at.desc()).all()
    return render_template('admin/careers.html', careers=careers)

@admin_bp.route('/careers/new', methods=['GET', 'POST'])
@login_required
def new_career():
    """Create new career path"""
    form = CareerPathForm()
    
    if form.validate_on_submit():
        career = CareerPath(
            title=form.title.data,
            description=form.description.data,
            icon_class=form.icon_class.data,
            icon_color=form.icon_color.data,
            skills=form.skills.data,
            salary_range=form.salary_range.data,
            learning_time=form.learning_time.data,
            order_index=form.order_index.data,
            is_active=form.is_active.data
        )
        db.session.add(career)
        db.session.commit()
        
        flash(f'Career path "{career.title}" created successfully!', 'success')
        return redirect(url_for('admin.careers'))
    
    return render_template('admin/career_form.html', form=form, title='New Career Path')

@admin_bp.route('/careers/<int:career_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_career(career_id):
    """Edit career path"""
    career = CareerPath.query.get_or_404(career_id)
    form = CareerPathForm(obj=career)
    
    if form.validate_on_submit():
        career.title = form.title.data
        career.description = form.description.data
        career.icon_class = form.icon_class.data
        career.icon_color = form.icon_color.data
        career.skills = form.skills.data
        career.salary_range = form.salary_range.data
        career.learning_time = form.learning_time.data
        career.order_index = form.order_index.data
        career.is_active = form.is_active.data
        career.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash(f'Career path "{career.title}" updated successfully!', 'success')
        return redirect(url_for('admin.careers'))
    
    return render_template('admin/career_form.html', form=form, career=career, title='Edit Career Path')

@admin_bp.route('/careers/<int:career_id>/delete', methods=['POST'])
@login_required
def delete_career(career_id):
    """Delete career path"""
    career = CareerPath.query.get_or_404(career_id)
    title = career.title
    
    db.session.delete(career)
    db.session.commit()
    
    flash(f'Career path "{title}" deleted successfully!', 'success')
    return redirect(url_for('admin.careers'))
