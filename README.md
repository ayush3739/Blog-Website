# BlogPy — A Full-Stack Flask Blog Website

<div align="center">

![BlogPy Banner](https://img.shields.io/badge/BlogPy-Hexon%20Dev-0085A1?style=for-the-badge&logo=flask&logoColor=white)

[![Live Demo](https://img.shields.io/badge/🌐_Live_Demo-blogpy.vercel.app-0085A1?style=flat-square)](https://blogpy.vercel.app)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3.2-000000?style=flat-square&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square&logo=bootstrap&logoColor=white)](https://getbootstrap.com)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com)

**BlogPy** is a fully functional, full-stack personal blog web application built with Flask. It supports user authentication, rich-text post creation, Gravatar-powered comments, social sharing, email contact, and is deployed live on Vercel.

[🌐 Live Website](https://blogpy.vercel.app) • [📂 Repository](https://github.com/ayush3739/Blog-Website) • [📋 Feature Ideas](./FEATURE_IDEAS.md)

</div>

---

## 📸 Website Screenshots

> Visit the live site at **[blogpy.vercel.app](https://blogpy.vercel.app)** to explore the full experience.

| Page | Description |
|---|---|
| **Home** | Lists all blog posts with title, subtitle, author, and date |
| **Post View** | Full post content with social share buttons and comments section |
| **New/Edit Post** | CKEditor-powered rich text editor (admin only) |
| **Register / Login** | Secure authentication with hashed passwords |
| **About** | Personal bio page |
| **Contact** | Contact form with live email delivery via Gmail SMTP |
| **404 / 500** | Custom styled error pages |

---

## ✨ Features

### 🔐 User Authentication & Profiles
- **Register / Login** with secure **PBKDF2-SHA256 password hashing**.
- **Secure Password Reset** via OTP sent securely to the user's email.
- **Dedicated User Profiles** showcasing user details, bio, and join date.
- **Admin role** automatically assigned to the first registered user.

### 📝 Blog Posts & Interactions
- **Rich-Text Post Creation** (Admin only) using CKEditor.
- **Categories & Tags** for organizing posts.
- **Reading Time Estimate** automatically calculated and displayed.
- **Pagination** for browsing through the blog archive.
- **Like & Bookmark Posts** with a dedicated Saved posts section on user profiles.

### 💬 Comments & Community
- **XSS-Protected Comments** sanitized strictly using Bleach.
- **Gravatar Integration** seamlessly fetches users' HTTPS-secured avatars based on email.

### 📤 Social Sharing & Contact
- **One-Click Share Buttons** for Twitter, LinkedIn, Facebook, and WhatsApp.
- **Live Contact Form** sending direct messages to admin via Gmail SMTP.

### 🎨 UI / UX Enhancements
- **Reading Progress Bar** & **Back to Top Button**.
- **Toast Notifications** for flash messages.
- **Confirmation Modals** for destructive actions (e.g., deleting posts) preventing accidental deletion.
- Fully responsive design using Bootstrap 5.

### 🛡️ Advanced Security & Reliability
- **CSRF Protection** applied strictly across sensitive forms (like post deletion).
- **Rate Limiting** via Flask-Limiter & Redis to prevent comment/OTP spam.
- **Custom Error Pages** (404 Not Found / 429 Too Many Requests / 500 Server Error).

### ☁️ Deployment
- Configured for **Vercel (serverless)** with Redis URL integration.
- Database ready for **PostgreSQL** integration (like Neon).

---

## 🗂️ Project Structure

```
Blog-Website/
│
├── main.py                  # Flask app, models, routes
├── forms.py                 # WTForms: Post, Register, Login, Comment
├── requirements.txt         # Python dependencies
├── vercel.json              # Vercel deployment config
├── .env                     # Environment variables (not committed)
├── FEATURE_IDEAS.md         # Planned feature improvements
│
├── templates/               # Jinja2 HTML templates
│   ├── header.html          # Navbar, toast, progress bar (shared)
│   ├── footer.html          # Footer, back-to-top, social links
│   ├── index.html           # Home page — post listing
│   ├── post.html            # Individual post view + comments
│   ├── make-post.html       # Create / Edit post form
│   ├── register.html        # Registration page
│   ├── login.html           # Login page
│   ├── about.html           # About Me page
│   ├── contact.html         # Contact form page
│   ├── 404.html             # Custom 404 error page
│   └── 500.html             # Custom 500 error page
│
└── static/
    ├── css/
    │   └── styles.css       # Custom styles + animations
    ├── js/
    │   └── scripts.js       # JS for progress bar, back-to-top, toasts
    └── assets/
        ├── img/             # Background images per page
        └── favicon.ico      # Site favicon
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, Flask 2.3.2 |
| **Database ORM** | Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0 |
| **Database** | SQLite (local / Vercel) · PostgreSQL (production) |
| **Authentication** | Flask-Login 0.6.3, Werkzeug (PBKDF2 hashing) |
| **Forms** | Flask-WTF 1.2.1, WTForms 3.0.1 |
| **Rich Text Editor** | Flask-CKEditor 0.4.6 |
| **Avatars** | Flask-Gravatar 0.5.0 |
| **Frontend** | Bootstrap 5, Bootstrap-Flask 2.2.0 |
| **Fonts & Icons** | Google Fonts (Lora, Open Sans), Font Awesome 6 |
| **Email** | Python `smtplib` + Gmail SMTP SSL |
| **Deployment** | Vercel (serverless) |
| **Environment** | python-dotenv 1.2.1 |

---

## 🚀 Getting Started (Local Setup)
 Framework** | Python 3.10+, Flask 2.3.2 |
| **Database & ORM** | Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0, Flask-Migrate (Alembic) |
| **Datastore** | SQLite (Local) / PostgreSQL (Production) |
| **Security & Auth** | Flask-Login, Flask-WTF (CSRF), Werkzeug, Bleach (XSS) |
| **Performance/Spam**| Flask-Limiter 4.1.1 backed by Redis 7.4.0 |
| **Forms & Editor** | WTForms 3.0.1, Flask-CKEditor 0.4.6 |
| **Avatars / UI** | Flask-Gravatar, Bootstrap 5, Bootstrap-Flask |
| **Email Services** | Python `smtplib` + Gmail SMTP SSL (for OTPs and Contact) |
| **Deployment** | Vercel (serverless infrastructure)
### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
secret_key=your_flask_secret_key

# Email (for Contact form)
email=your_gmail@gmail.com
pass=your_gmail_app_password
to_email=recipient@example.com

# Database (optional — defaults to SQLite)
DB_URI=sqlite:///posts.db
```

> **Note:** For Gmail, generate an [App Password](https://support.google.com/accounts/answer/185833) (2FA must be enabled).

### 5. Run the app

```bash
python main.py
```

Visit `http://127.0.0.1:5000` in your browser.

> The first user to register automatically becomes the **admin** and can create, edit, and delete posts.

---

## 🗃️ Database Models

### `User`
| Field | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Unique user ID |
| `email` | String(100) | Unique email address |
| `password` | String | Hashed password |
| `name` | String(1000) | Display name |
| `is_adm, `password`, `name` | Strings | Core credentials and display name |
| `bio` | String(1000) | User's profile bio |
| `created_at` | DateTime | When the user joined |
| `is_admin` | Boolean | True if user ID = 1 |
| *Relationships* | `posts`, `comments`, `likes`, `bookmarks` | Associated content records |

### `BlogPost`
| Field | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Unique post ID |
| `title`, `subtitle`, `body` | String/Text | Core blog content |
| `img_url` | String(250) | Header image URL |
| `category`, `tags` | Strings | Grouping and search metadata |
| `read_time` | Integer | Auto-calculated read time in minutes |
| `like_count` | Integer | Counter cache for likes |
| *Relationships* | `comments`, `likes`, `bookmarks` | `cascade="all, delete-orphan"` |

### Social Interactions (`Comments`, `Like`, `BookMark`)
Standard mapping tables containing:
- Primary key IDs
- Foreign Keys (`user_id`, `post_id` / `comment_author_id`, `post_id`)
- (For Comments): Sanitized `text` content and submission `date`.
## 🌐 Routes Overview

| Method | Route | Description | Auth Required |
|---|---|---|---|
| GET | `/` | Home — all posts | — |
| GET/POST | `/register` | User registration | — |
| GET/POST | `/login` | User login | — |
| GET | `/logout` | Logout current user | ✅ |
| GET/POST | `/post/<id>` | View post + comment | — (comment: ✅) |
| GET/POST | `/new-post` | Create a new post | 🔒 Admin only |
| GET/POST | `/edit-post/<id>` | Edit an existing post | 🔒 Admin only |
| GET | `/delete/<id>` | Delete a post | 🔒 Admin only |
| GET | `/about` | About Me page | — |
| GET/POST | `/contact` | Contact form | — (submit: ✅) |

---

## 🔧 Environment Variables

| Variable | Description |
|---|---|
| `secret_key` | Flask secret key for sessions/CSRF |
| `email` | Gmail address for sending contact emails |
| `pass` | Gmail App Password |
| `to_email` | Email address that receives contact messages |
| `DB_URI` | Database URI (SQLite or PostgreSQL) |
| `VERCEL` | Set automatically by Vercel; switches DB path to `/tmp` |

---

## 📋 Planned Features

See [`FEATURE_IDEAS.md`](./FEATURE_IDEAS.md) for the full roadmap. Highlights include:

- [ ] Search posts by title/content
- [ ] Categories & Tags
- [ ] Reading Time Estimate
- [ ] Pagination
- [ ] Like / Bookmark posts
- [ ] User Profile pagesRemaining ideas include:

- [ ] Search posts by title/content
- [ ] Comment Replies (nested threads)
- [ ] Admin Dashboard
- [ ] Image Upload (Cloudinary / AWS S3)
- [ ] Newsletter Subscription

Recently Implemented ✅:
- [x] Categories & Tags
- [x] Reading Time Estimate
- [x] Pagination for all posts
- [x] Like / Bookmark posts
- [x] User Profile pages (with Member Since & Bios)
- [x] Forgot Password / OTP Email Flow
- [x] CSRF, Rate Limiting (Redis), & XSS Sanitization (Bleach)
- [x] Custom Error Pages (404, 429, 500
> *"Hexon Dev — learning software engineering one concept at a time."*

[![GitHub](https://img.shields.io/badge/GitHub-ayush3739-181717?style=flat-square&logo=github)](https://github.com/ayush3739)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Ayush%20Maurya-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/ayush-maurya-b39914315)
[![Email](https://img.shields.io/badge/Email-ayushmaurya21086@gmail.com-EA4335?style=flat-square&logo=gmail&logoColor=white)](mailto:ayushmaurya21086@gmail.com)

---

## 📄 License

This project is open source. Feel free to fork, explore, and build upon it.

---

<div align="center">
  <strong>Built with ❤️ using Flask & Bootstrap</strong><br>
  © 2025 Ayush Maurya
</div>
