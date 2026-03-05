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

### 🔐 User Authentication
- **Register** with name, email, and password
- Passwords are securely **hashed using PBKDF2-SHA256** (via Werkzeug)
- **Login / Logout** with Flask-Login session management
- Duplicate email detection with user-friendly flash messages
- **Admin role** — the first registered user (ID = 1) becomes an admin with elevated privileges

### 📝 Blog Posts (Admin Only)
- **Create new posts** with title, subtitle, image URL, and rich-text body
- **Edit existing posts** — pre-filled form with current content
- **Delete posts** — one-click post deletion directly from the home page
- Posts are **ordered by newest first**
- Posts display author name and formatted date

### 💬 Comments
- Any **logged-in user** can leave comments on posts
- Comments use **CKEditor** (rich text) for formatting
- **Gravatar integration** — commenter avatars auto-generated from email
- Unauthenticated users are redirected to login before commenting

### 📤 Social Sharing
- Each blog post includes share buttons for:
  - 🐦 **Twitter / X**
  - 💼 **LinkedIn**
  - 📘 **Facebook**
  - 💬 **WhatsApp**
  - 🔗 **Copy Link** to clipboard

### 📬 Contact Form
- Sends real emails via **Gmail SMTP** (SSL, port 465)
- Captures: Name, Email, Phone, Message
- **Login-required** to submit (submit button disabled for guests)
- Success/error feedback with flash messages

### 🎨 UI / UX Enhancements
- **Reading Progress Bar** — Fixed at the top, fills as you scroll through a post
- **Back to Top Button** — Floating button that appears on scroll
- **Toast Notifications** — Animated slide-in flash messages (top-right corner)
- **Smooth Page Transitions** — CSS fade-in animations between pages
- **Post Card Hover Effects** — Lift/shadow animation on home page post previews
- **Responsive Design** — Fully mobile-friendly via Bootstrap 5
- **Google Fonts** — Lora & Open Sans for clean typography

### 🛡️ Custom Error Pages
- **404 Not Found** — Friendly ghost icon, links to Home and Contact
- **500 Server Error** — Warning icon, option to retry or go Home

### ☁️ Deployment
- Deployed on **Vercel** (serverless)
- SQLite in `/tmp` on Vercel (ephemeral), or **PostgreSQL** via environment variable (`DB_URI`, `DATABASE_URL`, `POSTGRES_URL`, etc.)
- Supports **Neon PostgreSQL** integration

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

### Prerequisites
- Python 3.10+
- `pip`

### 1. Clone the repository

```bash
git clone https://github.com/ayush3739/Blog-Website.git
cd Blog-Website
```

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
| `is_admin` | Boolean | True if user ID = 1 |
| `posts` | Relationship | Posts authored by user |
| `comments` | Relationship | Comments left by user |

### `BlogPost`
| Field | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Unique post ID |
| `author_id` | FK → User | Author reference |
| `title` | String(250) | Post title (unique) |
| `subtitle` | String(250) | Post subtitle |
| `date` | String(250) | Formatted post date |
| `body` | Text | Full HTML post content |
| `img_url` | String(250) | Header image URL |

### `Comments`
| Field | Type | Description |
|---|---|---|
| `id` | Integer (PK) | Unique comment ID |
| `author_id` | FK → User | Comment author |
| `post_id` | FK → BlogPost | Parent post |
| `text` | Text | Comment body (HTML) |
| `date` | DateTime | Timestamp |

---

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
- [ ] User Profile pages
- [ ] Comment Replies (nested threads)
- [ ] Admin Dashboard
- [ ] Image Upload (Cloudinary / AWS S3)
- [ ] Newsletter Subscription

Already implemented ✅:
- [x] Reading Progress Bar
- [x] Back to Top Button
- [x] Custom Error Pages (404, 500)
- [x] Post Card Hover Effects
- [x] Share Buttons (Twitter, LinkedIn, Facebook, WhatsApp, Copy Link)

---

## 👤 Author

**Ayush Maurya**

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
