# CMS Manager Django

A professional, bilingual (Persian/English) product catalog and content management system built with Django.

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-4.x-green.svg)](https://djangoproject.com)

---

## Features

- **Full Product Management** – Add, edit, and organize products with categories, name, short/long descriptions, price, discount price, stock quantity, SKU, and custom technical specifications (key/value table).

- **Multi-Image Upload** – Upload multiple images simultaneously from the same add/edit form. The first image is automatically set as the primary image. After upload, you can reorder images, change the primary image, or delete individual images directly from the admin panel.

- **Automatic QR Code Generation** – Enter your store URL in the Store Settings section of the admin panel, and a QR Code is automatically generated and displayed in the footer of every page — allowing customers to scan and visit your store instantly.

- **Bilingual (Persian/English)** – All products and categories have separate fields for Persian and English content. URLs follow `/fa/...` and `/en/...` patterns, with a language switcher in the header. Page direction (RTL/LTR) switches automatically based on the selected language.

- **Dark/Light Theme** – A theme toggle button in the header saves the user's preference in a cookie (works without JavaScript).

- **Professional Product Page** – Image gallery (primary image + clickable thumbnails), price with discount display, stock status, technical specifications table, full description, and related products — similar to professional online stores.

- **Category Browsing & Search** – Category pages with sidebar navigation, sorting by price/newest, pagination, and product search functionality.

---

## Tech Stack

- **Backend:** Django 4.x, Python 3.10+
- **Database:** SQLite (default), PostgreSQL / MySQL supported for production
- **Frontend:** HTML, CSS, JavaScript (minimal), Bootstrap-like custom styling
- **Localization:** Django's `gettext` with compiled translation files (.po/.mo)
- **QR Code:** `qrcode` library for automatic QR generation

---

## Prerequisites

- Python 3.10 or higher
- `gettext` tool installed on your system (for translation compilation)
  - Linux: `sudo apt install gettext`
  - macOS: `brew install gettext`
  - Windows: Install via [gettext for Windows](https://mlocati.github.io/articles/gettext-iconv-windows.html)

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/GoldenIsland00/CMS_manager_Django.git
cd CMS_manager_Django
```

### 2. Create and Activate a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate      # On Linux/macOS
# venv\Scripts\activate       # On Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py migrate
```

### 5. Compile Translation Files

```bash
python manage.py compilemessages
```

### 6. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

Then access:

- **Frontend:** [http://127.0.0.1:8000/fa/](http://127.0.0.1:8000/fa/) (or `/en/` for English)
- **Admin Panel:** [http://127.0.0.1:8000/fa/admin/](http://127.0.0.1:8000/fa/admin/)

---

## First Steps After Installation

1. Log in to the admin panel and go to **Store Settings / تنظیمات فروشگاه**. Enter your store name, slogan, logo, contact number, and most importantly, the **Store URL** — the QR Code will be generated automatically.

2. Go to **Categories / دسته‌بندی‌ها** and create some categories (e.g., "Electronics", "Clothing"...).

3. Go to **Products / محصولات** and add a new product:
   - Enter name, short description, and full description in both languages.
   - Set price and (optionally) discount price.
   - In the "Upload images / آپلود تصاویر" section, select multiple images at once.
   - After saving, add technical specifications (e.g., weight, volume, country of origin) in the "Specifications / مشخصات فنی" section.

---

## Project Structure

```
shop_cms/
├── manage.py
├── requirements.txt
├── shop_cms/              # Project settings and main URLs
├── core/                  # Store settings, QR Code generation, theme toggle, homepage
├── products/              # Categories, products, images, technical specifications
├── templates/             # HTML templates (base, home, category, product detail)
├── static/                # CSS and JavaScript files
└── locale/                # Persian/English translation files
```

---

## Production Deployment Notes

> **Important:** The `shop_cms/settings.py` file is currently configured for development. Before deploying to a production server:

1. **Replace `SECRET_KEY`** with a strong, random value (never keep the default).

2. **Set `DEBUG = False`**.

3. **Restrict `ALLOWED_HOSTS`** to your actual domain(s):
   ```python
   ALLOWED_HOSTS = ["example.com", "www.example.com"]
   ```

4. **Use PostgreSQL or MySQL** instead of SQLite for production databases.

5. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```
   Then serve them via your web server (Nginx, Apache, etc.).

6. **Enable HTTPS** on your production server.

---

## Adding or Updating Translations

If you add new static text to templates using `{% trans "..." %}` tags, follow these steps to apply Persian translations:

```bash
python manage.py makemessages -l fa
# Edit the translation strings in locale/fa/LC_MESSAGES/django.po
python manage.py compilemessages
```

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## Author

**GoldenIsland00** – [GitHub Profile](https://github.com/GoldenIsland00)

---

## Acknowledgments

- Built with [Django](https://djangoproject.com)
- QR Code generation powered by [qrcode](https://pypi.org/project/qrcode/)
- Icons and design inspiration from modern e-commerce platforms
