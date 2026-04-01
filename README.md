# BlogPy — Full-Stack Flask Blog Website

<div align="center">
  <img src="static/assets/favicon.svg" alt="BlogPy Logo" width="72" height="72" />

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
<img src="static/assets/favicon.svg" alt="BlogPy Logo" width="56" height="56" />

### Landing Page Screenshot
Add your landing-page image at `static/assets/landing-page.png`, then replace this section with:

<!-- ![Landing Page](static/assets/landing-page.png) -->

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

## 🌐 Application Routes

| Method | Route | Access | Notes |
|---|---|---|---|
| GET | `/` | Public | Home feed + trending |
| GET | `/all-posts` | Public | Search/sort/filter + pagination |
| GET/POST | `/register` | Public | User signup |
| GET/POST | `/login` | Public | User login |
| GET | `/logout` | Login required | Ends session |
| GET/POST | `/forgot-password` | Public | Request OTP |
| GET/POST | `/verify-password` | Public | Verify OTP |
| GET/POST | `/reset-password` | Public (session-gated) | Reset password after OTP |
| GET/POST | `/post/<post_id>` | Public (comment: login required) | Post view + comments/replies |
| GET/POST | `/new-post` | Login required | Post creation form |
| GET/POST | `/edit-post/<post_id>` | Login + owner/admin | Edit post |
| POST | `/delete/<post_id>` | Login + owner/admin | Delete post |
| POST | `/like/<post_id>` | Login required | Toggle like |
| POST | `/bookmark/<post_id>` | Login required | Toggle bookmark |
| GET | `/profile` | Login required | Current user profile |
| GET/POST | `/edit-profile` | Login required | Update profile |
| GET | `/about` | Public | About page |
| GET/POST | `/contact` | Public | Contact form |
| POST | `/newsletter-subs` | Public | Newsletter subscription |
| GET | `/favicon.ico` | Public | Redirects favicon asset |
| GET | `/too-many-requests` | Public | 429 page |
| GET | `/debug/user/<user_id>` | Admin only | Debug endpoint |

## 🗃️ Database Models

- `User`: `id`, `email`, `password`, `name`, `bio`, `is_admin`, `created_at`
- `BlogPost`: `id`, `author_id`, `title`, `subtitle`, `body`, `img_url`, `date`, `read_time`, `like_count`, `category_id`
- `Comments`: `id`, `parent_id`, `author_id`, `post_id`, `text`, `created_at`
- `Like`: composite key (`user_id`, `post_id`)
- `BookMark`: composite key (`user_id`, `post_id`)
- `Category`: `id`, `name`
- `Tag`: `id`, `name`
- `NewsletterSubs`: `id`, `email`, `date_subscribed`
- Association table: `post_tags` for BlogPost ↔ Tag many-to-many mapping

## 🧱 Tech Stack
- **Backend:** Flask, SQLAlchemy, Flask-Login, Flask-WTF
- **Database:** SQLite (local), PostgreSQL-compatible URI support
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
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
   For Windows:
   ```bash
   venv\Scripts\activate
   ```
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
