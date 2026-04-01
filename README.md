# BlogPy — Full-Stack Flask Blog Website

<div align="center">
  <img src="static/assets/favicon.svg" alt="BlogPy Logo" width="110" />

  [![Live Demo](https://img.shields.io/badge/Live_Demo-blogpy.vercel.app-0085A1?style=flat-square)](https://blogpy.vercel.app)
  [![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
  [![Flask](https://img.shields.io/badge/Flask-2.3.2-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
  [![Deployed on Vercel](https://img.shields.io/badge/Deployed_on-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com)
</div>

BlogPy is a full-stack personal blogging platform built with Flask, SQLAlchemy, and Bootstrap/Tailwind styling support.
It includes authentication, post management, comments, likes/bookmarks, profile management, newsletter subscriptions, OTP-based password reset, and production deployment support.

## 🔗 Links
- Live: https://blogpy.vercel.app
- Repo: https://github.com/ayush3739/Blog-Website

## 🖼️ Branding & Screenshots

### Website Logo (SVG)
![BlogPy Logo](static/assets/favicon.svg)

### Landing Page Screenshot
Add your landing-page image at `static/assets/landing-page.png` and then add this line under this section:

`![Landing Page](static/assets/landing-page.png)`

## ✨ Features

### Authentication & User Management
- User registration and login
- Secure password hashing (Werkzeug)
- Forgot password flow with OTP email verification
- Password reset after OTP verification
- Admin role support (`is_admin`)
- User profile page
- Profile editing (name, email, bio)
- Member-since timestamp tracking

### Blog Content Management
- Create, edit, and delete blog posts
- Rich text editor via CKEditor
- Category support
- Multi-tag support (many-to-many)
- Automatic read-time estimation
- Author ownership checks for edit/delete

### Discovery, Search & Navigation
- Home feed with newest posts
- Trending posts based on like count
- Dedicated all-posts page
- Search posts by title/subtitle
- Sort by newest, oldest, or likes
- Filter by category and tag
- Pagination for posts

### Community & Engagement
- Commenting system on posts
- Nested comments/replies support
- XSS-safe comment sanitization with Bleach
- Like/unlike posts
- Bookmark/unbookmark posts
- Comment pagination for better readability

### Newsletter & Contact
- Newsletter email subscriptions
- Duplicate subscription protection
- Contact form with SMTP-based email sending

### Security, Stability & Platform
- CSRF protection via Flask-WTF
- Rate limiting with Flask-Limiter
- Redis-compatible limiter backend support
- Custom error pages for 404, 429, 500
- AJAX-aware rate-limit handling
- Vercel deployment configuration
- Flexible DB environment support (SQLite/Postgres)
- Automatic category/tag seeding at startup

## 🧱 Tech Stack
- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Database:** SQLite (local), Postgres-compatible URI support
- **Frontend:** Jinja templates, Bootstrap 5, Tailwind CSS tooling
- **Editor:** Flask-CKEditor
- **Security/Quality:** Bleach, Flask-Limiter, CSRF protections
- **Email:** SMTP utilities for contact and OTP flows
- **Deployment:** Vercel

## 📁 Project Structure

```text
Blog-Website/
├── main.py
├── models.py
├── forms.py
├── utils.py
├── requirements.txt
├── package.json
├── vercel.json
├── static/
│   ├── assets/
│   │   ├── favicon.svg
│   │   └── ...
│   ├── css/
│   └── js/
└── templates/
```

## 🚀 Local Setup
1. Create and activate virtual environment
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Install frontend tooling:
   ```bash
   npm install
   npm run build:css
   ```
4. Configure environment variables in `.env`:
   - `secret_key`
   - `email`
   - `pass`
   - `to_email`
   - `DATABASE_URL` (optional)
5. Run:
   ```bash
   python main.py
   ```

## 📄 License
Open source — feel free to fork and build on it.
