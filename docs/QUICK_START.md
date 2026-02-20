# Quick Start Guide - Environment Setup

## For First-Time Contributors

### 1. Clone and Setup
```bash
# Clone the repository
git clone <repository-url>
cd <project-directory>

# Install dependencies
pip install -r requirements.txt
```

### 2. Create Environment File
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your local settings
# Open .env in your editor and fill in the required values
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 5. Start Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` in your browser.

---

## Environment Variables Quick Reference

### Required for Development
- `DEBUG=True` - Enable debug mode locally
- `SECRET_KEY` - Django secret (auto-generated, change for production)

### Email Settings (Optional for Local Development)
- `EMAIL_HOST_USER` - Your email address
- `EMAIL_HOST_PASSWORD` - Your email password/app password
- `EMAIL_RECIPIENT` - Default recipient email

### Database (Default: SQLite)
- `DB_ENGINE=django.db.backends.sqlite3`
- `DB_NAME=db.sqlite3`

For MySQL/PostgreSQL, see `ENV_SETUP.md` for detailed configuration.

---

## Common Issues

### Error: "ModuleNotFoundError: No module named 'dotenv'"
```bash
pip install python-dotenv
# or reinstall requirements
pip install -r requirements.txt
```

### Error: "SECRET_KEY does not match"
- Ensure `.env` file exists in project root
- Check that `load_dotenv()` is being called in settings.py

### Email Not Working
- Check `EMAIL_HOST_USER` and `EMAIL_HOST_PASSWORD` in `.env`
- For Gmail: Use App Passwords (https://myaccount.google.com/apppasswords)
- Ensure 2FA is enabled on your Gmail account first

---

## File by File

| File | Purpose |
|------|---------|
| `.env` | **NEVER COMMIT** - Your local environment configuration |
| `.env.example` | Template for developers - safe to commit |
| `ENV_SETUP.md` | Comprehensive environment setup guide |
| `SECURITY_AUDIT.md` | Security changes made to the project |
| `requirements.txt` | Python dependencies (includes python-dotenv) |
| `ecommerce/settings.py` | Django settings (now reads from .env) |

---

## Before Committing Code

Run these checks:
```bash
# Check for syntax errors
python -m py_compile main/views.py dashboard/views.py

# Run tests (if any)
python manage.py test

# Verify .env is NOT committed
git status  # Should NOT show .env
```

---

## Support

- See `ENV_SETUP.md` for advanced configuration
- See `SECURITY_AUDIT.md` for what was changed
- Check Django docs: https://docs.djangoproject.com/
