# Shishir Portfolio Website

A professional portfolio website for graphic designer Shishir Kandel, featuring animated homepage elements, comprehensive portfolio management, and admin functionality.

## 🚀 Quick Start (Local Development)

### 1. Download and Setup
```bash
# Extract the shishir-website folder
cd shishir-website

# Install dependencies
pip install -r requirements.txt

# Setup portfolio data
python setup_portfolio.py

# Run the application
python app.py
```

### 2. Access the Website
- **Main Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login
- **Login**: username=`admin`, password=`admin123`

## 📤 GitHub Deployment

### 1. Create GitHub Repository
1. Create a new repository on GitHub called `shishir-portfolio`
2. Set it to Public

### 2. Upload Files
```bash
# Navigate to your shishir-website folder
cd shishir-website

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial portfolio website deployment"

# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/shishir-portfolio.git

# Push to GitHub
git push -u origin main
```

## 🌐 Vercel Deployment

### 1. Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click "New Project"
4. Import your `shishir-portfolio` repository

### 2. Configure Settings
- **Framework**: Other
- **Root Directory**: `./`
- **Build Command**: (leave empty)
- **Output Directory**: (leave empty)

### 3. Environment Variables
Add these in Vercel dashboard:
- `SECRET_KEY`: `your-secret-key-2025`
- `DATABASE_URL`: (optional - uses SQLite by default)

### 4. Deploy
Click "Deploy" and wait for completion!

## 📁 Project Structure

```
shishir-website/
├── api/app.py              # Vercel entry point
├── static/
│   ├── css/               # Stylesheets
│   ├── js/                # JavaScript
│   ├── images/            # Site images
│   └── uploads/           # Portfolio images
├── templates/             # HTML templates
├── app.py                 # Main Flask app
├── models.py              # Database models
├── admin.py               # Admin panel
├── views.py               # Public routes
├── forms.py               # Form definitions
├── requirements.txt       # Dependencies
└── setup_portfolio.py     # Portfolio setup script
```

## 🎨 Features

### Portfolio Management
- ✅ File upload support (JPG, PNG, GIF)
- ✅ Image URL support
- ✅ CSRF protection fixed
- ✅ Category organization
- ✅ Featured projects
- ✅ Custom ordering

### Admin Panel
- ✅ Secure login system
- ✅ Portfolio management
- ✅ Contact form handling
- ✅ Site settings
- ✅ Analytics tracking

### Frontend
- ✅ Responsive design
- ✅ Animated elements
- ✅ Blue color scheme
- ✅ Modern UI/UX

## 🔧 Admin Panel Usage

### Adding Portfolio Items
1. Go to `/admin/login`
2. Login with admin credentials
3. Navigate to Portfolio → Add New Project
4. Fill in project details
5. Upload image or paste URL
6. Save project

### Managing Content
- **Remove Expert Education**: Already handled in setup
- **Update Study in Canada**: Use the new uploaded image
- **Add new projects**: Use the portfolio form

## 🐛 Troubleshooting

### CSRF Token Error
✅ **Fixed**: All forms now include proper CSRF tokens

### Images Not Loading
1. Check file exists in `/static/uploads/`
2. Verify image URL in admin panel
3. Ensure proper file permissions

### Local Testing Issues
```bash
# If you get import errors
pip install -r requirements.txt

# If database issues
python setup_portfolio.py

# If port already in use
python app.py  # Will use port 5000
```

### Deployment Issues
1. Verify all files are in GitHub repository
2. Check Vercel environment variables
3. Ensure vercel.json is configured correctly

## 📞 Support

If you encounter any issues:
1. Check the console logs in your browser
2. Verify all files are uploaded to GitHub
3. Test locally first: `python app.py`
4. Check Vercel deployment logs

## 🎯 Your URLs After Deployment

- **Live Website**: `https://your-repo-name.vercel.app`
- **Admin Panel**: `https://your-repo-name.vercel.app/admin/login`

---

**Your professional portfolio website is ready for deployment! 🎉**