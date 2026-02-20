# Environment Configuration Guide

## Overview
This project uses environment variables to manage sensitive configuration. All sensitive data should be stored in a `.env` file, NOT in the code.

## Setup Instructions

### 1. Create Local Environment File
```bash
cp .env.example .env
```

### 2. Install Dependencies
First, install python-dotenv and other dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configure .env File
Edit the `.env` file with your local configuration:

```env
# Django Settings
DEBUG=True  # Set to False in production
SECRET_KEY=your-very-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Email Configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_RECIPIENT=recipient@gmail.com

# Security (set to True in production with HTTPS)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

## Environment Variables

### Django Settings
- **DEBUG**: Set to `False` in production
- **SECRET_KEY**: Use a strong, random key. Generate with: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- **ALLOWED_HOSTS**: Comma-separated list of allowed hosts

### Database Configuration
- **DB_ENGINE**: Database backend (sqlite3, mysql, postgresql)
- **DB_NAME**: Database name or file path
- **DB_USER**: Database username (for MySQL/PostgreSQL)
- **DB_PASSWORD**: Database password (for MySQL/PostgreSQL)
- **DB_HOST**: Database host (for MySQL/PostgreSQL)
- **DB_PORT**: Database port (for MySQL/PostgreSQL)

### Email Configuration
- **EMAIL_HOST**: SMTP server (e.g., smtp.gmail.com)
- **EMAIL_USE_TLS**: Use TLS (True/False)
- **EMAIL_PORT**: SMTP port (e.g., 587 for Gmail)
- **EMAIL_HOST_USER**: Email address for sending emails
- **EMAIL_HOST_PASSWORD**: Email password or app password
- **EMAIL_RECIPIENT**: Default recipient email

### Security Settings
- **SECURE_SSL_REDIRECT**: Redirect HTTP to HTTPS (True/False)
- **SESSION_COOKIE_SECURE**: Only send cookies over HTTPS (True/False)
- **CSRF_COOKIE_SECURE**: Only send CSRF cookie over HTTPS (True/False)

## Gmail Configuration

For Gmail SMTP:
1. Enable "Less secure app access" or use App Passwords
2. Create an App Password: https://myaccount.google.com/apppasswords
3. Use the app password for `EMAIL_HOST_PASSWORD`

## Production Deployment

When deploying to production:

1. Generate a new SECRET_KEY
2. Set `DEBUG=False`
3. Set `SECURE_SSL_REDIRECT=True`
4. Set `SESSION_COOKIE_SECURE=True`
5. Set `CSRF_COOKIE_SECURE=True`
6. Configure proper `ALLOWED_HOSTS`
7. Use PostgreSQL or MySQL instead of SQLite
8. Set up proper email configuration
9. Use a `.env` file with production credentials (securely managed by your hosting provider)

## Security Best Practices

✅ **DO:**
- Store `.env` in `.gitignore`
- Use strong, randomly generated SECRET_KEY
- Use App Passwords for Gmail instead of your actual password
- Keep `.env` file on the server (not in version control)
- Use environment-specific `.env` files (.env.production, .env.development)
- Rotate credentials regularly

❌ **DON'T:**
- Commit `.env` file to Git
- Share `.env` file via email or public channels
- Hardcode secrets in Python files
- Use generic or weak passwords
- Push production credentials to version control

## Troubleshooting

### .env file not being loaded
- Make sure `python-dotenv` is installed: `pip install python-dotenv`
- Ensure `.env` file is in the project root directory
- Restart your development server

### ImportError: No module named 'dotenv'
```bash
pip install python-dotenv
```

### Email not sending
- Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Verify SMTP settings for your email provider
- Check Django logs for detailed error messages

## References
- [Django Environment Variables](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [python-dotenv Documentation](https://github.com/theskumar/python-dotenv)
