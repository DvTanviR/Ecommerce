# Static Images Directory - Standard File Naming Guide

This directory contains all essential images for your e-commerce platform. To customize with your own branding, simply replace the standardized file names listed below.

## 📋 Standard File Naming Convention

All files use **simple, descriptive names** for easy identification and replacement. This allows you to customize the platform without touching any code.

---

## 🎯 Essential Files (MUST REPLACE)

These files are visible to end-users. You should replace them with your own branding:

### 1. **logo.png** (2.2 KB)
- **Purpose:** Main logo used in navigation header and footer
- **Used In:** 
  - Header navigation
  - Footer branding
  - Dashboard header
- **Recommended Size:** 200px × 50px PNG with transparent background
- **Action:** ✅ **Replace with your company logo**

**How to Replace:**
```bash
cp your_logo.png static/assets/img/logo.png
```

### 2. **favicon.ico** (1.2 KB)
- **Purpose:** Browser tab icon
- **Used In:** All pages (browser tab)
- **Recommended Size:** 32px × 32px ICO or PNG
- **Action:** ✅ **Replace with your company favicon**

**How to Replace:**
```bash
cp your_favicon.ico static/assets/img/favicon.ico
```

### 3. **about-header.jpg** (81 KB)
- **Purpose:** Hero/header image for About page
- **Used In:** About page background
- **Recommended Size:** 1920px × 600px JPG
- **Action:** ✅ **Replace with your company about photo**

**How to Replace:**
```bash
cp your_about_header.jpg static/assets/img/about-header.jpg
```

### 4. **about-image-1.jpg** (81 KB)
- **Purpose:** Main about page company image
- **Used In:** About page (right side image)
- **Recommended Size:** 500px × 500px JPG
- **Action:** ✅ **Replace with your company image**

**How to Replace:**
```bash
cp your_about_image_1.jpg static/assets/img/about-image-1.jpg
```

### 5. **about-image-2.jpg** (81 KB)
- **Purpose:** Secondary about page company image
- **Used In:** About page (overlay behind main image)
- **Recommended Size:** 500px × 500px JPG
- **Action:** ✅ **Replace with your company secondary image**

**How to Replace:**
```bash
cp your_about_image_2.jpg static/assets/img/about-image-2.jpg
```

---

## 🔧 Utility Files (KEEP AS-IS)

These files are used for functionality and UI elements. Keep them as-is unless you have custom requirements:

### error-bg.jpg (17 KB)
- **Purpose:** Error page background image
- **Used In:** 404/error pages
- **Customization:** Optional - customize if you want unique error pages

### placeholder.webp (8.2 KB)
- **Purpose:** Fallback image for broken/missing product images
- **Used In:** Product carousel error handling
- **Customization:** Optional - replace with your placeholder

### placeholder2.webp (9.8 KB)
- **Purpose:** Alternative placeholder (currently unused)
- **Used In:** Generated for future use
- **Customization:** Can be deleted or reused

### add-to-cart.png (14 KB)
- **Purpose:** Add to cart button icon (if used)
- **Used In:** Cart functionality
- **Customization:** Optional

---

## 📁 Related Static Directories

### Brand Images: `/static/assets/images/brands/`
Contains brand/partner logos:
- 1.png, 2.png, 3.png, 4.png, 5.png, 6.png (brand carousel)

**Where Used:** Brand carousel on homepage
**Customization:** Replace with your partner/brand logos

### Dashboard Assets: `/static/dashboard/assets/img/`
Contains admin dashboard images (separate from main site)
- Already synced with logo.png and favicon.ico

---

## 🚀 Quick Customization Checklist

To fully customize your branding:

```bash
# 1. Navigate to static/assets/img directory
cd static/assets/img/

# 2. Replace the 5 essential files:
cp /path/to/your/logo.png .
cp /path/to/your/favicon.ico .
cp /path/to/your/about-header.jpg .
cp /path/to/your/about-image-1.jpg .
cp /path/to/your/about-image-2.jpg .

# 3. (Optional) Replace brand images
cd ../images/brands/
cp /path/to/your/brand/logos/*.png .

# 4. Verify changes
# Clear browser cache with Ctrl+F5
# Test all pages
```

---

## 📐 Recommended Image Specifications

### Logo
- **Format:** PNG with transparent background (or SVG)
- **Size:** 200px × 50px (width × height)
- **File Size:** < 50 KB
- **Color:** Match your brand colors

### Favicon
- **Format:** ICO or PNG
- **Size:** 32px × 32px minimum
- **File Size:** < 10 KB
- **Note:** Most browsers will automatically convert PNG to ICO

### About Header
- **Format:** JPG (for compression)
- **Size:** 1920px × 600px recommended
- **File Size:** < 200 KB
- **Aspect Ratio:** 16:9

### About Images (1 & 2)
- **Format:** JPG (for photo quality)
- **Size:** 500px × 500px
- **File Size:** < 150 KB each
- **Type:** Professional photos of your company/team

### Brand Logos
- **Format:** PNG with transparent background
- **Size:** 150px × 150px
- **File Size:** < 50 KB each
- **Colors:** Keep consistent style

---

## ⚙️ Technical Details

### Image Optimization
All images in this directory should be optimized for web:

```bash
# Optimize JPG
convert about-header.jpg -strip -interlace Plane -quality 85 about-header.jpg

# Optimize PNG
pngquant 256 logo.png -o logo.png

# Convert to WebP for better compression
cwebp logo.png -o logo.webp
```

### Image References in Code
Images are referenced using Django's `{% static %}` template tag:

```html
<!-- Logo -->
<img src="{% static 'assets/img/logo.png' %}" alt="Logo">

<!-- Favicon -->
<link rel="icon" href="{% static 'assets/img/favicon.ico' %}">

<!-- About images -->
<img src="{% static 'assets/img/about-image-1.jpg' %}">
```

**No code changes needed** - just replace the files with the same names!

---

## 🔐 File Safety Notes

### What NOT to Do
- ❌ Don't rename files without updating code
- ❌ Don't store credentials or sensitive info
- ❌ Don't use images larger than 2MB
- ❌ Don't use uncommon file formats

### What TO Do
- ✅ Keep original backup copies
- ✅ Optimize images for web
- ✅ Use standard formats (JPG, PNG, ICO)
- ✅ Maintain aspect ratios
- ✅ Test on different devices

---

## 🐛 Troubleshooting

### Logo Not Showing?
```bash
# Verify file exists
ls -la static/assets/img/logo.png

# Collect static files
python manage.py collectstatic --noinput

# Clear browser cache (Ctrl+F5)
```

### Favicon Not Updating?
- Clear browser cache completely
- Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)
- Allow up to 24 hours for CDN update

### Images Appear Stretched?
- Check recommended dimensions above
- Ensure proper aspect ratio
- Test with browser zoom (100%)

### File Size Too Large?
```bash
# Use online tools or ImageMagick to compress
# Online: https://tinypng.com/ or https://imageoptim.com/
# Command line: convert image.jpg -quality 80 image-optimized.jpg
```

---

## 📊 Current File Inventory

| File | Size | Purpose | Status |
|------|------|---------|--------|
| logo.png | 2.2 KB | Header logo | ✅ Ready to replace |
| favicon.ico | 1.2 KB | Tab icon | ✅ Ready to replace |
| about-header.jpg | 81 KB | About page header | ✅ Ready to replace |
| about-image-1.jpg | 81 KB | About page main | ✅ Ready to replace |
| about-image-2.jpg | 81 KB | About page secondary | ✅ Ready to replace |
| error-bg.jpg | 17 KB | Error page | Keep as-is |
| placeholder.webp | 8.2 KB | Fallback image | Keep as-is |
| placeholder2.webp | 9.8 KB | Unused | Optional |
| add-to-cart.png | 14 KB | UI element | Keep as-is |

---

## ✨ Best Practices

1. **Always backup originals** before replacing
2. **Test after replacement** on multiple devices
3. **Optimize before uploading** to reduce load time
4. **Use consistent styling** across all images
5. **Document your changes** for team reference
6. **Keep version control** of image assets
7. **Monitor file sizes** to ensure good performance

---

## 🔗 External Resources

- **Image Compression:** https://tinypng.com/
- **Favicon Generator:** https://realfavicongenerator.net/
- **Image Optimization:** https://imageoptim.com/
- **Icon Fonts:** https://fontawesome.com/
- **Image CDN:** https://imagekit.io/

---

## 📞 Support

For issues with image replacement:

1. **Check file exists:** `ls -la static/assets/img/logo.png`
2. **Verify file permissions:** `chmod 755 static/assets/img/logo.png`
3. **Clear Django cache:** `python manage.py collectstatic --clear --noinput`
4. **Empty browser cache:** Press Ctrl+Shift+Delete and clear all

---

## ✅ Summary

This directory now uses **clean, standardized file naming** that allows anyone to customize branding by simply **replacing files** - **no code changes needed!**

**Just drop your files in with the standard names and you're done! 🚀**
