# Shishir Portfolio Website - Complete Deployment Guide

## 📁 Project Structure
```
shishir-website/
├── api/
│   └── app.py              # Vercel entry point
├── static/
│   ├── css/                # All stylesheets
│   ├── js/                 # JavaScript files
│   ├── images/             # Design assets
│   └── uploads/            # Portfolio images
├── templates/
│   ├── admin/              # Admin panel templates
│   ├── base.html           # Base template
│   ├── index.html          # Homepage
│   └── ...                 # Other templates
├── app.py                  # Main Flask application
├── models.py               # Database models
├── admin.py                # Admin routes
├── views.py                # Public routes
├── forms.py                # Form definitions
├── config.py               # Configuration
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
└── vercel.json             # Vercel deployment config
```

## 🚀 Local Development Setup

### 1. Prerequisites
- Python 3.9+ installed
- Git installed

### 2. Local Testing
```bash
cd shishir-website
pip install -r requirements.txt
python app.py
```

Your website will be available at: http://localhost:5000

### 3. Admin Panel Access
- URL: http://localhost:5000/admin/login
- Username: admin
- Password: admin123

## 📤 GitHub Repository Setup

### 1. Create GitHub Repository
1. Go to GitHub.com
2. Click "New Repository"
3. Name: `shishir-portfolio`
4. Set to Public
5. Don't initialize with README (we have files)

### 2. Upload to GitHub
```bash
cd shishir-website
git init
git add .
git commit -m "Initial portfolio website with admin panel"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/shishir-portfolio.git
git push -u origin main
```

## 🌐 Vercel Deployment (Recommended)

### 1. Connect GitHub to Vercel
1. Go to vercel.com
2. Sign up with GitHub
3. Click "New Project"
4. Import your `shishir-portfolio` repository

### 2. Configure Environment Variables
In Vercel dashboard, add these environment variables:
- `SECRET_KEY`: `your-secret-key-here-2025`
- `DATABASE_URL`: (optional - uses SQLite if not provided)

### 3. Deploy Settings
- Framework Preset: Other
- Root Directory: `./`
- Build Command: (leave empty)
- Output Directory: (leave empty)
- Install Command: `pip install -r requirements.txt`

### 4. Custom Domain (Optional)
1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS setup instructions

## 🗄️ Database Options

### Option 1: SQLite (Free - Default)
- Automatically uses SQLite database
- Perfect for small portfolios
- No additional setup required

### Option 2: PostgreSQL (Production)
1. Create free database at:
   - Railway.app
   - Supabase.com
   - PlanetScale.com
2. Add `DATABASE_URL` environment variable in Vercel

## 🔧 Troubleshooting Common Issues

### CSRF Token Error
✅ **Fixed in code** - All forms include proper CSRF tokens

### Images Not Loading
- Ensure all images are in `/static/uploads/` directory
- Check file paths in portfolio admin panel
- Verify image file extensions (jpg, png, gif)

### 404 Errors
- Ensure `vercel.json` routes are configured correctly
- Check that all template files exist in `/templates/`

### 403 Forbidden Errors
- Verify environment variables are set in Vercel
- Check file permissions (should be readable)

## 📝 Content Management

### Adding Portfolio Projects
1. Go to `/admin/login`
2. Navigate to Portfolio → Add New Project
3. Upload image, add title and description
4. Save and publish

### Managing Website Content
- **Site Settings**: Admin → Settings
- **Contact Messages**: Admin → Contacts  
- **Analytics**: Admin → Analytics

## 🔄 Making Updates

### Code Changes
1. Make changes to your local files
2. Test locally: `python app.py`
3. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update website"
   git push
   ```
4. Vercel automatically redeploys

### Adding New Images
1. Use admin panel: Admin → Portfolio → Add New Project
2. Or manually add to `/static/uploads/` folder

## 📊 Performance Optimization

### Image Optimization
- Use compressed JPG for photos
- Use PNG for graphics with transparency
- Recommended max size: 1MB per image

### SEO
- Update meta descriptions in Admin → Settings
- Add alt text to all images
- Use descriptive file names

## 🆘 Support

### If Something Goes Wrong
1. Check Vercel deployment logs
2. Test locally first: `python app.py`
3. Verify all files are committed to GitHub
4. Check environment variables in Vercel dashboard

### Portfolio Not Showing Images
1. Go to Admin → Portfolio
2. Edit each project
3. Re-upload images if needed
4. Ensure image URLs start with `/static/uploads/`

## ✅ Success Checklist

- [ ] Local development works (`python app.py`)
- [ ] GitHub repository created and code pushed
- [ ] Vercel project created and deployed
- [ ] Environment variables configured
- [ ] Admin panel accessible (/admin/login)
- [ ] Portfolio images displaying correctly
- [ ] Contact form working
- [ ] Mobile responsive design verified

## 🎯 Your Website URLs

After deployment:
- **Live Website**: `https://your-project-name.vercel.app`
- **Admin Panel**: `https://your-project-name.vercel.app/admin/login`
- **Portfolio API**: `https://your-project-name.vercel.app/api/portfolio`

---

**Congratulations! Your professional portfolio website is now live! 🎉**