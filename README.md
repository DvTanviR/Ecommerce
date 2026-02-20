# YourBrand E-Commerce Platform

A modern, white-label Django-based e-commerce platform designed for fashion and general retail businesses. Production-ready with comprehensive security, scalability, and customization options.

**Status:** ✅ Production Ready  |  **License:** Open Source  |  **Django Version:** 4.0.2

---

## 🎯 Features

### Core Features
- ✅ **Product Management** - Full CRUD operations with image galleries
- ✅ **Category Management** - Organize products by categories
- ✅ **Shopping Cart** - Persistent cart with session management
- ✅ **Order Management** - Regular and card payment checkouts
- ✅ **User Management** - Registration, profile, order history
- ✅ **Reviews & Ratings** - Product reviews with moderation
- ✅ **Admin Dashboard** - Full admin panel with analytics
- ✅ **Blog System** - Post/comment management with CKEditor
- ✅ **Flash Deals** - Time-based promotional features
- ✅ **White-Label Ready** - Easy customization for any brand

### Technical Features
- 🔒 **Security First** - Environment-based configuration, SSL/TLS ready
- 📧 **Email Integration** - SMTP configured for notifications
- 🗄️ **Database Flexible** - SQLite (dev), MySQL/PostgreSQL (production)
- 📱 **Responsive Design** - Bootstrap-based, mobile-friendly
- ⚡ **Performance Optimized** - Static file optimization, query optimization
- 🔍 **SEO Ready** - Proper URL structures and metadata

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Local Setup](#local-setup)
4. [Customization](#customization)
5. [Production Deployment](#production-deployment)
6. [Admin Dashboard](#admin-dashboard)
7. [Database Management](#database-management)
8. [Troubleshooting](#troubleshooting)
9. [Documentation](#documentation)
10. [Support](#support)

---

## 🚀 Quick Start

**For the impatient:**

```bash
# Clone/Download project
cd "path/to/project"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp docs/ENV_SETUP.md .env  # Review and edit .env file

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Start development server
python manage.py runserver

# Visit: http://127.0.0.1:8000
```

---

## 💻 System Requirements

### Minimum Requirements
- **Python:** 3.9 or higher
- **RAM:** 1 GB (development), 2 GB (production)
- **Storage:** 500 MB
- **OS:** Linux, macOS, or Windows

### Development
- Python 3.9+
- pip or conda
- Git
- Virtual environment tool (venv)

### Production (VPS)
- Python 3.9+
- Web Server: Nginx or Apache
- Application Server: Gunicorn or uWSGI
- Database: PostgreSQL 10+ or MySQL 5.7+
- SSL Certificate: Let's Encrypt (free)
- Memory: 2GB+ recommended
- CPU: 1+ cores

---

## 📥 Local Setup

### Step 1: Download & Extract

```bash
# Option A: Clone from Git
git clone <repository-url>
cd "Open source"

# Option B: Download and extract ZIP
unzip ecommerce-platform.zip
cd "Open source"
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp docs/ENV_SETUP.md .env

# Edit .env with your configuration
# Important settings to update:
# - SECRET_KEY: Keep as is or generate new
# - DEBUG: True (for development)
# - ALLOWED_HOSTS: localhost, 127.0.0.1
# - DATABASE: sqlite3 is fine for dev
# - EMAIL settings: For notifications
```

**Key .env Variables:**
```bash
DEBUG=True                          # Set to False in production
SECRET_KEY=<your-secret-key>       # Never share this
ALLOWED_HOSTS=localhost,127.0.0.1  # Add your domain
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### Step 5: Setup Database

```bash
# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Follow prompts:
# Username: admin
# Email: your-email@example.com
# Password: strong-password

# Collect static files
python manage.py collectstatic --noinput
```

### Step 6: Run Locally

```bash
# Start development server
python manage.py runserver

# You should see:
# Starting development server at http://127.0.0.1:8000/
```

**Access the site:**
- 🏠 Homepage: http://127.0.0.1:8000/
- 🔧 Admin Panel: http://127.0.0.1:8000/admin
- 📱 Dashboard: http://127.0.0.1:8000/dashboard

**Login:**
- Username: admin
- Password: (the password you created)

---

## 🎨 Customization

### Branding (Logo & Favicon)

1. **Replace Logo:**
   - File: `static/assets/img/logo.png` (2.2 KB, PNG)
   - Used in: Header, footer, dashboard sidebar, favicon
   - Just copy your logo with the same filename - **no code changes needed**

2. **Replace Favicon:**
   - File: `static/assets/img/favicon.ico` (1.2 KB, ICO)
   - Appears in: Browser tab
   - Format: .ico file

3. **About Page Images:**
   - `static/assets/img/about-header.jpg` - Hero image
   - `static/assets/img/about-image-1.jpg` - Company photo 1
   - `static/assets/img/about-image-2.jpg` - Company photo 2

4. **Dashboard Branding:**
   - Edit: `templates/dashboard/header.html` - Change "YourBrand" text
   - Logo automatically uses `static/assets/img/logo.png`

### Site Configuration

1. **Site Name & Description:**
   - Edit: `templates/main.html` (line ~5)
   ```html
   <title>YourBrand - Online Shopping</title>
   ```

2. **Contact Information:**
   - Edit: `templates/footer.html` - Update phone, email, address
   - Or use environment variables in `.env`

3. **Colors & Styling:**
   - Edit: `static/assets/css/style.css`
   - Main colors typically defined as CSS variables

4. **Email Templates:**
   - Edit: `main/views.py` - Email message content
   - Modify order confirmation, password reset emails

### Homepage Content

**Flash Deals:**
- Go to: 🔧 Dashboard → Template → **FlashDeal Management**
- Create/edit flash deal with image and promotional text

**Trending Products:**
- Dashboard → Template → Edit TrendCover
- Set trending product section image and link

**Featured Products:**
- Dashboard → Template → Edit Featured Products
- Select products to display in featured section

**Category Management:**
- Dashboard → Categories → Add/Edit categories
- Products appear automatically in category pages

---

## 🚀 Production Deployment (VPS)

Complete guide for deploying to a VPS server (DigitalOcean, Linode, AWS, etc.)

### Prerequisites
- VPS with Ubuntu 20.04+ (or similar Linux distro)
- Domain name (optional but recommended)
- SSH access to VPS
- Basic Linux knowledge

### Step 1: VPS Initial Setup

```bash
# SSH into your VPS
ssh root@your-vps-ip

# Update system
apt update && apt upgrade -y

# Install Python and dependencies
apt install -y python3 python3-pip python3-venv \
    postgresql postgresql-contrib nginx git supervisor

# Create project user (security best practice)
useradd -m -s /bin/bash ecommerce
```

### Step 2: Clone & Setup Project

```bash
# Switch to project user
sudo -u ecommerce -H bash

# Navigate to home
cd ~

# Clone project
git clone <repository-url> project

# Go to project directory
cd project

# Create virtual environment
python3 -m venv venv

# Activate venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Add production packages
pip install gunicorn psycopg2-binary python-dotenv
```

### Step 3: Configure PostgreSQL Database

```bash
# Switch to root or use sudo
sudo -u postgres psql

# Create database and user
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'your-strong-password';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

### Step 4: Configure Environment for Production

```bash
# Navigate to project
cd /home/ecommerce/project

# Edit .env file
nano .env

# Update these critical settings:
```

**Production .env Configuration:**
```bash
# Django Settings
DEBUG=False                                    # CRITICAL: Set to False
SECRET_KEY=your-super-secret-key-here        # Generate new
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-vps-ip

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=your-strong-password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_RECIPIENT=orders@yourdomain.com

# Security Settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
```

### Step 5: Setup Django for Production

```bash
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Test if everything works
python manage.py check

# Test Gunicorn
gunicorn ecommerce.wsgi:application --bind 127.0.0.1:8000
# Should not show errors; press Ctrl+C to stop
```

### Step 6: Configure Gunicorn (Application Server)

```bash
# Create Gunicorn service file
sudo nano /etc/systemd/system/gunicorn.service
```

**Paste this content:**
```ini
[Unit]
Description=Gunicorn application server for ERS Fashion
After=network.target

[Service]
Type=notify
User=ecommerce
WorkingDirectory=/home/ecommerce/project
ExecStart=/home/ecommerce/project/venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --timeout 60 \
    ecommerce.wsgi:application

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start Gunicorn
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```

### Step 7: Configure Nginx (Web Server)

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/ecommerce
```

**Paste this content:**
```nginx
upstream gunicorn_app {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;

    # SSL Certificates (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # SSL Security Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    client_max_body_size 20M;

    location /static/ {
        alias /home/ecommerce/project/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias /home/ecommerce/project/media/;
        expires 7d;
    }

    location / {
        proxy_pass http://gunicorn_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }
}
```

```bash
# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/ecommerce /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site

# Test Nginx configuration
sudo nginx -t

# Start Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Step 8: Setup SSL Certificate (Let's Encrypt)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Update Nginx with certificate paths (automatic with certbot --nginx)
sudo certbot renew --dry-run

# Auto-renew (crontab)
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### Step 9: Verify Production Setup

```bash
# Check services
sudo systemctl status gunicorn
sudo systemctl status nginx

# Check logs
journalctl -u gunicorn -n 20
sudo tail -f /var/log/nginx/error.log

# Test the site
curl https://yourdomain.com
```

Visit: https://yourdomain.com in your browser

---

## 📊 Admin Dashboard

**Access:** https://your-site.com/dashboard

### Key Features

1. **Product Management**
   - Add/Edit/Delete products
   - Manage product images
   - Set prices and inventory

2. **Order Management**
   - View all orders
   - Track order status
   - Export order data

3. **Template Management**
   - **FlashDeal** - Create promotional features
   - **TrendCover** - Set trending products
   - **FeaturedProducts** - Highlight best sellers
   - **CoverSell** - Manage banner images

4. **Blog Management**
   - Create/edit blog posts
   - Moderate comments
   - Categories and tags

5. **Reviews & Ratings**
   - Approve/reject reviews
   - Manage ratings

---

## 🗄️ Database Management

### Local Development (SQLite)
- **Automatic:** SQLite is configured by default
- **File:** `db.sqlite3` in project root
- **Backup:** Simply copy `db.sqlite3`

### Production (PostgreSQL)

**Backup:**
```bash
pg_dump ecommerce_db > backup-$(date +%Y%m%d).sql
```

**Restore:**
```bash
psql ecommerce_db < backup-20260220.sql
```

### Migrations

```bash
# Create migration
python manage.py makemigrations

# Apply migration
python manage.py migrate

# View migration history
python manage.py showmigrations
```

---

## 🔧 Common Tasks

### Create Admin User
```bash
python manage.py createsuperuser
```

### Reset Admin Password
```bash
python manage.py changepassword admin
```

### Backup Database
```bash
# Development
cp db.sqlite3 db.backup.sqlite3

# Production
pg_dump ecommerce_db > backup.sql
```

### Clear Static Files Cache
```bash
python manage.py collectstatic --clear --noinput
```

### View Database Tables
```bash
python manage.py dbshell
```

---

## ⚡ Troubleshooting

### Site Not Loading Locally
```bash
# Check if port 8000 is available
netstat -tlnp | grep 8000

# Kill process using port 8000
lsof -ti:8000 | xargs kill -9

# Restart server
python manage.py runserver
```

### Static Files Not Loading
```bash
# Recollect static files
python manage.py collectstatic --clear --noinput

# Check permissions
ls -la staticfiles/
```

### Database Errors
```bash
# Rollback migration
python manage.py migrate <app> <migration_number>

# Reset migrations (WARNING: loses data)
python manage.py migrate --fake <app> zero
python manage.py migrate <app>
```

### ModuleNotFoundError
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### 500 Error in Production
```bash
# Check Django logs
journalctl -u gunicorn -n 50

# Check Nginx logs
sudo tail -50 /var/log/nginx/error.log

# Verify DEBUG=False in settings
grep DEBUG ecommerce/settings.py
```

---

## 📚 Documentation

Additional detailed documentation available in the `docs/` folder:

- **[docs/ENV_SETUP.md](docs/ENV_SETUP.md)** - Environment configuration guide
- **[docs/SECURITY_AUDIT.md](docs/SECURITY_AUDIT.md)** - Security implementation details
- **[docs/QUICK_START.md](docs/QUICK_START.md)** - Quick reference guide
- **[docs/WHITE_LABEL_BRANDING.md](docs/WHITE_LABEL_BRANDING.md)** - Branding customization

---

## 🎓 Project Structure

```
project-root/
├── ecommerce/              # Main Django config
│   ├── settings.py        # Configuration (uses .env)
│   ├── urls.py           # Main URLs
│   └── wsgi.py          # WSGI for production
├── main/                  # Main app (products, orders, etc)
│   ├── models.py         # Database models
│   ├── views.py          # Business logic
│   ├── urls.py           # App-specific URLs
│   └── migrations/       # Database migrations
├── dashboard/            # Admin dashboard app
│   ├── views.py          # Dashboard logic
│   ├── forms.py          # Admin forms
│   └── urls.py           # Dashboard URLs
├── templates/            # Django HTML templates
│   ├── home/            # Homepage sections
│   ├── dashboard/       # Admin templates
│   └── main.html        # Base template
├── static/              # Static files (CSS, JS, images)
│   ├── assets/         # General assets
│   └── dashboard/      # Dashboard assets
├── media/              # User-uploaded files
├── docs/               # Documentation
├── manage.py           # Django management
├── requirements.txt    # Python dependencies
├── .env               # Environment configuration (NOT in git)
└── README.md          # This file
```

---

## 🔒 Security Checklist for Production

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate new `SECRET_KEY`
- [ ] Use strong admin password
- [ ] Configure HTTPS/SSL certificate
- [ ] Set up email authentication
- [ ] Enable SQL injection protection
- [ ] Setup CSRF protection
- [ ] Configure XSS protection
- [ ] Setup database backups
- [ ] Monitor logs regularly
- [ ] Keep dependencies updated: `pip install --upgrade -r requirements.txt`

---

## 📞 Support & Contributing

**Issues & Questions:**
- Check [docs/](docs/) folder for detailed guides
- Review error logs in production
- Consult Django documentation: https://docs.djangoproject.com/

**Contributing:**
- Improvements welcome
- Submit pull requests
- Report bugs with details

---

## 📄 License

This project is licensed under the **MIT License**.

You are free to:
- ✅ Use this commercially
- ✅ Modify the code
- ✅ Distribute copies
- ✅ Use privately

Required:
- 📋 Include the license and copyright notice
- 📋 Include a disclaimer

For full license details, see [LICENSE](LICENSE) file.

**Attribution Example:**
```
This project uses YourBrand E-Commerce Platform
Licensed under the MIT License
```

Learn more: https://opensource.org/licenses/MIT

---

## 🙏 Acknowledgments

Built with:
- **Django 4.0.2** - Web framework
- **Bootstrap** - UI Framework
- **PostgreSQL** - Database
- **Nginx** - Web server
- **Gunicorn** - Application server

---

## 🚀 Next Steps

1. **Local Testing**
   ```bash
   python manage.py runserver
   # Visit http://127.0.0.1:8000
   ```

2. **Customize**
   - Replace logo and favicon
   - Update site name and colors
   - Configure email
   - Add products and categories

3. **Deploy**
   - Follow [VPS Deployment](#production-deployment) section
   - Setup SSL certificate
   - Configure domain

4. **Go Live**
   - Add real products
   - Setup payment gateway
   - Configure email notifications
   - Monitor performance

---

**Last Updated:** February 20, 2026  
**Current Version:** 1.0.0  
**Django:** 4.0.2  
**Python:** 3.9+
