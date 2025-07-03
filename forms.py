from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, HiddenField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    """Admin login form"""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')

class ContactForm(FlaskForm):
    """Contact form for frontend"""
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    subject = StringField('Subject', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])
    phone = StringField('Phone', validators=[Optional(), Length(max=20)])
    company = StringField('Company', validators=[Optional(), Length(max=100)])

class PageForm(FlaskForm):
    """Page creation/editing form"""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    slug = StringField('Slug', validators=[DataRequired(), Length(max=100)])
    content = TextAreaField('Content', validators=[Optional()])
    meta_description = TextAreaField('Meta Description', validators=[Optional(), Length(max=500)])
    meta_keywords = StringField('Meta Keywords', validators=[Optional(), Length(max=500)])
    template_name = SelectField('Template', choices=[
        ('page.html', 'Default Page'),
        ('index.html', 'Home Page'),
    ], default='page.html')
    is_published = BooleanField('Published', default=True)
    is_featured = BooleanField('Featured')

class SiteConfigForm(FlaskForm):
    """Site configuration form"""
    site_title = StringField('Site Title', validators=[Optional(), Length(max=200)])
    site_description = TextAreaField('Site Description', validators=[Optional(), Length(max=500)])
    contact_email = StringField('Contact Email', validators=[Optional(), Email()])
    contact_phone = StringField('Contact Phone', validators=[Optional(), Length(max=20)])
    contact_location = StringField('Contact Location', validators=[Optional(), Length(max=100)])
    hero_title = StringField('Hero Title', validators=[Optional(), Length(max=200)])
    hero_subtitle = TextAreaField('Hero Subtitle', validators=[Optional(), Length(max=500)])
    about_title = StringField('About Section Title', validators=[Optional(), Length(max=200)])
    about_content = TextAreaField('About Content', validators=[Optional(), Length(max=2000)])
    social_twitter = StringField('Twitter URL', validators=[Optional()])
    social_linkedin = StringField('LinkedIn URL', validators=[Optional()])
    social_github = StringField('GitHub URL', validators=[Optional()])
    social_instagram = StringField('Instagram URL', validators=[Optional()])
    social_facebook = StringField('Facebook URL', validators=[Optional()])
    social_behance = StringField('Behance URL', validators=[Optional()])
    submit = SubmitField('Save Settings')

class PortfolioForm(FlaskForm):
    """Portfolio project form"""
    title = StringField('Project Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    image_url = StringField('Image URL', validators=[Optional(), Length(max=500)])
    image_file = FileField('Upload Image', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')])
    project_url = StringField('Project URL', validators=[Optional(), Length(max=500)])
    category = SelectField('Category', choices=[
        ('graphic-design', 'Graphic Design'),
        ('web-design', 'Web Design'),
        ('branding', 'Branding'),
        ('print-design', 'Print Design'),
        ('social-media', 'Social Media'),
        ('ui-ux', 'UI/UX Design'),
        ('educational-design', 'Educational Design'),
        ('service-design', 'Service Design'),
        ('healthcare-design', 'Healthcare Design'),
        ('corporate-design', 'Corporate Design'),
        ('cultural-design', 'Education Consultancy'),
        ('other', 'Other')
    ], default='graphic-design')
    tags = StringField('Tags', validators=[Optional(), Length(max=500)])
    is_featured = BooleanField('Featured Project')
    order_index = IntegerField('Display Order', validators=[Optional()], default=0)
    submit = SubmitField('Save Project')

class SkillForm(FlaskForm):
    """Skill form"""
    name = StringField('Skill Name', validators=[DataRequired(), Length(max=100)])
    category = SelectField('Category', choices=[
        ('Design Software', 'Design Software'),
        ('Design Specializations', 'Design Specializations'),
        ('Additional Skills', 'Additional Skills')
    ], default='Design Software')
    icon_class = StringField('Icon Class', validators=[Optional(), Length(max=100)])
    color = StringField('Color', validators=[Optional(), Length(max=20)], default='#8b5cf6')
    proficiency = IntegerField('Proficiency (%)', validators=[Optional(), NumberRange(min=0, max=100)], default=80)
    order_index = IntegerField('Display Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Skill')

class CareerPathForm(FlaskForm):
    """Career path form"""
    title = StringField('Career Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=1000)])
    icon_class = StringField('Icon Class', validators=[Optional(), Length(max=100)])
    icon_color = StringField('Icon Color', validators=[Optional(), Length(max=100)], 
                           default='linear-gradient(135deg, #8b5cf6, #ec4899)')
    skills = TextAreaField('Skills', validators=[Optional()])
    salary_range = StringField('Salary Range', validators=[Optional(), Length(max=100)])
    learning_time = StringField('Learning Time', validators=[Optional(), Length(max=100)])
    order_index = IntegerField('Display Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save Career Path')
