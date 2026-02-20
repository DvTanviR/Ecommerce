# White Label Branding Guide

This e-commerce platform has been converted to a white-label solution, removing all original company branding. This guide explains how to customize it with your own branding.

## Quick Start Customization Checklist

- [ ] Update site name and tagline
- [ ] Replace logo and favicon
- [ ] Update contact information
- [ ] Configure email settings
- [ ] Update footer information
- [ ] Customize color scheme (optional)
- [ ] Update social media links
- [ ] Deploy and test

## 1. **Update Site Branding Globally**

### Site Name and Title
Located in: `templates/main.html`, `templates/header.html`, `templates/footer.html`

**Default:** "YourBrand"

Replace all instances of `YourBrand` with your company name:
- Page titles
- Meta descriptions
- Site taglines

### Example Configuration Variables

Create a file `config/branding.py`:
```python
# config/branding.py
SITE_NAME = "My Mobile Store"
SITE_TAGLINE = "Quality Products, Great Prices"
COMPANY_NAME = "My Company LLC"
WEBSITE_URL = "https://mystore.com"
```

Update `settings.py` to include:
```python
SITE_NAME = os.getenv('SITE_NAME', 'YourBrand')
SITE_TAGLINE = os.getenv('SITE_TAGLINE', 'Mobile & Accessories')
```

Then pass to templates via context processor.

---

## 2. **Replace Logo and Favicon**

### Logo Files
The platform uses the following logo references:
- **Header Logo:** `static/assets/img/logo.png` (150px width)
- **Footer Logo:** `static/assets/img/logo.png`
- **Favicon:** `static/assets/img/logo.png`
- **About Page Images:** `static/assets/img/about-image-1.jpg` and `about-image-2.jpg`

### Files That Reference Logos
- `templates/main.html` - Favicon references
- `templates/header.html` - Header logo
- `templates/footer.html` - Footer logo
- `templates/dashboard/main.html` - Dashboard favicon
- `templates/dashboard/header.html` - Dashboard logo
- `templates/home/about.html` - About page images

### What to Replace
1. **Logo (PNG, SVG, or JPG):**
   - Recommended: 200x50px for header
   - Format: PNG with transparent background
   - File: `static/assets/img/logo.png`

2. **Favicon (32x32):**
   - File: `static/assets/img/logo.png` (or create `favicon.ico`)
   - PNG or ICO format

3. **About Page Images:**
   - `static/assets/img/about-image-1.jpg` (Main image)
   - `static/assets/img/about-image-2.jpg` (Secondary image)
   - Recommended: 500x500px JPG

**Steps:**
```bash
# Replace files in static directory
cp /path/to/your/logo.png static/assets/img/logo.png
cp /path/to/your/favicon.ico static/assets/img/favicon.ico
cp /path/to/your/about1.jpg static/assets/img/about-image-1.jpg
cp /path/to/your/about2.jpg static/assets/img/about-image-2.jpg
```

---

## 3. **Update Contact Information**

### Replace Generic Contact Details

**Current default contact number:** `+1-800-123-4567`
**Current default email:** `info@yourstore.com`

### Files to Update
Replace the placeholder contact info in these files:

1. **`templates/header.html`** - Phone number in header
2. **`templates/footer.html`** - Company information
3. **`templates/home/contact.html`** - Contact form page
4. **`templates/home/about.html`** - About page
5. **`templates/home/index.html`** - Homepage

### Search and Replace
```bash
# Find all occurrences
grep -r "+1-800-123-4567" templates/
grep -r "info@yourstore.com" templates/

# Replace with your info
sed -i 's/+1-800-123-4567/YOUR_PHONE/g' templates/**/*.html
sed -i 's/info@yourstore.com/your@email.com/g' templates/**/*.html
```

### Contact Information Variables

Update `.env`:
```env
SITE_PHONE=+1-800-123-4567
SITE_EMAIL=info@yourstore.com
SITE_ADDRESS="123 Main St, City, Country"
SITE_CITY="Your City"
SITE_COUNTRY="Your Country"
```

---

## 4. **Email Configuration**

### Email Branding in Notifications

**Files to update:**
- `main/views.py` - Email subject lines and messages

### Current Email Templates
1. **Order Notification Email**
   - Subject: "New Order Received from: {name}"
   - File: `main/views.py` (line ~430, ~796)

2. **Contact Form Response**
   - Subject: "Thanks for contacting us"
   - File: `main/views.py` (line ~512)

### Customize Email Messages
```python
# main/views.py example
subject = f"Order Confirmation - {SITE_NAME}"
message = f"Thank you for your order at {SITE_NAME}. ..."
```

---

## 5. **Update Footer Information**

### Footer Content
Located in: `templates/footer.html`

**Default text:** "Your trusted online store for quality smartphones, accessories, and mobile products. Shop with confidence."

### Customize:
```html
<!-- templates/footer.html -->
<p>YOUR_COMPANY_DESCRIPTION</p>
<p>Copyright ©2025 YOUR_COMPANY_NAME. All Rights Reserved.</p>
```

### Social Media Links
**Current defaults:** Placeholder links (`href="#"`)

Replace with your actual social media URLs:
```html
<!-- Facebook, Instagram, Twitter, etc. -->
<a href="https://facebook.com/yourpage" target="_blank">
  <i class="icon-facebook-f"></i>
</a>
```

---

## 6. **Meta Tags and SEO**

### Update Descriptions

**Files to check:**
- `templates/main.html` - Main meta tags
- `templates/header.html` - Header meta tags
- `templates/footer.html` - Footer meta tags
- `templates/home/*.html` - Individual page tags

### Example Updates
```html
<meta name="description" content="YOUR_COMPANY_NAME - Buy quality mobile products at great prices.">
<meta name="keywords" content="mobile shop, smartphones, accessories, YOUR_CITY">
<meta name="author" content="YOUR_COMPANY_NAME">
```

### Update in Context
```python
# main/context_processors.py
def site_context(request):
    return {
        'site_name': os.getenv('SITE_NAME', 'YourBrand'),
        'site_description': os.getenv('SITE_DESCRIPTION', 'Quality mobile products'),
        'company_email': os.getenv('COMPANY_EMAIL', 'info@yourstore.com'),
        'company_phone': os.getenv('COMPANY_PHONE', '+1-800-123-4567'),
    }
```

Then use in templates:
```html
<meta name="description" content="{{ site_description }}">
<a href="tel:{{ company_phone }}">{{ company_phone }}</a>
```

---

## 7. **Color Scheme Customization**

### Main CSS Files
- `static/assets/css/style.css` - Main styles
- `static/assets/css/theam.css` - Theme color
- `static/assets/css/skins/skin-demo-4.css` - Skin colors

### Update CSS Variables (if using modern approach)
```css
/* static/assets/css/custom.css */
:root {
    --primary-color: #007bff;      /* Your primary color */
    --secondary-color: #6c757d;    /* Your secondary color */
    --success-color: #28a745;      /* Your success color */
    --danger-color: #dc3545;       /* Your error color */
}
```

### Brand Colors
Find and replace common color patterns:
- **Primary Color:** Look for `#0a5c9c` or similar
- **Secondary Color:** Look for `#666666` or similar

---

## 8. **About Page Customization**

### Location in Templates
File: `templates/home/about.html`

### Update These Sections
1. **Vision Statement** - Your company's vision
2. **Mission Statement** - Your company's mission
3. **Company Description** - Who you are
4. **Testimonials** - Customer reviews (customize or keep generic)
5. **Images** - Replace about-image-1.jpg and about-image-2.jpg

### Example:
```html
<!-- Update Vision -->
<p>Our vision is to provide the best mobile shopping experience...</p>

<!-- Update Mission -->
<p>Our mission is to deliver quality products at affordable prices...</p>

<!-- Update About Section -->
<p>We are a trusted online retailer specializing in mobile products...</p>
```

---

## 9. **Environment Variables for Easy Branding**

Add these to `.env` for centralized configuration:

```env
# Brand Identity
BRAND_NAME=YourBrand
BRAND_TAGLINE=Quality Products, Great Value
COMPANY_NAME=Your Company LLC
COMPANY_DESCRIPTION=Your company description here

# Contact Information
COMPANY_EMAIL=info@yourstore.com
COMPANY_PHONE=+1-800-123-4567
COMPANY_ADDRESS=123 Main Street
COMPANY_CITY=Your City
COMPANY_STATE=Your State
COMPANY_COUNTRY=Your Country
COMPANY_ZIP=12345

# Social Media
FACEBOOK_URL=https://facebook.com/yourpage
INSTAGRAM_URL=https://instagram.com/yourpage
TWITTER_URL=https://twitter.com/yourpage

# Branding Colors (optional)
PRIMARY_COLOR=#007bff
SECONDARY_COLOR=#6c757d
```

---

## 10. **Category Customization**

### Product Categories
These are managed through Django admin:
1. Go to Django admin: `/admin/`
2. Navigate to "Categories"
3. Update category names and descriptions to match your products

Remember to update:
- Category names
- Category descriptions
- Category slugs (if using URL routing)

---

## 11. **Header & Navigation Customization**

### Update Navigation Links
File: `templates/header.html` and `templates/main.html`

### Navigation Menu Items
Current items:
- Home
- Shop
- Sell
- Top products
- Account
- Pages (Contact, About, Blog)

Customize in templates or via settings.

---

## 12. **Deploy and Test**

### After Customization

1. **Collect Static Files:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Clear Cache:**
   ```bash
   python manage.py clear_cache  # If using cache
   ```

3. **Test All Pages:**
   - [ ] Homepage
   - [ ] About page
   - [ ] Contact page
   - [ ] Product pages
   - [ ] Footer links
   - [ ] Email notifications

4. **Browser Testing:**
   - [ ] Logo displays correctly
   - [ ] Footer copyright shows your company name
   - [ ] Contact info is correct
   - [ ] Social media links work
   - [ ] Meta tags are accurate

---

## 13. **Advanced: Template Context Processor**

Create a context processor to pass branding data to all templates:

```python
# main/context_processors.py
import os
from django.conf import settings

def branding(request):
    """Add branding context to all templates"""
    return {
        'site_name': os.getenv('BRAND_NAME', 'YourBrand'),
        'site_tagline': os.getenv('BRAND_TAGLINE', 'Quality Products'),
        'company_email': os.getenv('COMPANY_EMAIL', 'info@yourstore.com'),
        'company_phone': os.getenv('COMPANY_PHONE', '+1-800-123-4567'),
        'company_address': os.getenv('COMPANY_ADDRESS', '123 Main St'),
        'facebook_url': os.getenv('FACEBOOK_URL', '#'),
        'instagram_url': os.getenv('INSTAGRAM_URL', '#'),
        'twitter_url': os.getenv('TWITTER_URL', '#'),
    }
```

Then add to `settings.py`:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.catagory_list_context',
                'main.context_processors.branding',  # Add this line
            ],
        },
    },
]
```

---

## 14. **File Replacement Checklist**

| File | Current | Replace With |
|------|---------|--------------|
| `static/assets/img/logo.png` | Placeholder | Your logo (PNG) |
| `static/assets/img/favicon.ico` | Placeholder | Your favicon (ICO/PNG) |
| `static/assets/img/about-image-1.jpg` | Placeholder | Your image |
| `static/assets/img/about-image-2.jpg` | Placeholder | Your image |
| `.env` | Template values | Your actual values |
| Site title | "YourBrand" | Your brand name |
| Footer text | "Your trusted online store" | Your tagline |

---

## 15. **Troubleshooting**

### Issue: Logo not showing
- **Solution:** Check if image path is correct in static files directory
- Run: `python manage.py collectstatic --noinput`

### Issue: Email still showing old company name
- **Solution:** Check `.env` variables are loaded
- Restart server: `python manage.py runserver`

### Issue: Meta tags not updating
- **Solution:** Check browser cache or hard refresh (Ctrl+F5)
- Verify template context processor is added

---

## 16. **Additional Resources**

- Django Documentation: https://docs.djangoproject.com/
- Static Files Guide: https://docs.djangoproject.com/en/stable/howto/static-files/
- Templates Guide: https://docs.djangoproject.com/en/stable/topics/templates/

---

## Summary of Changes Made

✅ **Removed:** All "Sanee Mobile" branding references
✅ **Updated:** Generic "YourBrand" placeholders throughout
✅ **Replaced:** Specific contact information with generic placeholders
✅ **Updated:** All email messages and notifications
✅ **Changed:** Logo references to generic `logo.png`
✅ **Updated:** Footer copyright and descriptions
✅ **Removed:** Specific Facebook and social media links

**Your e-commerce platform is now ready to be white-labeled with your own branding!**
