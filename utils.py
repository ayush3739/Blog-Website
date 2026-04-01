import os
import smtplib
import redis
from email.message import EmailMessage
import random

blogpy_email = os.getenv("email")  # Your BlogPy email address
app_password = os.getenv("pass")   # App password for BlogPy email

# Vercel Upstash may expose REDIS_URL or REDIS_KV_URL.
_redis_url = (
    os.getenv("REDIS_URL") or
    os.getenv("REDIS_KV_URL") or
    "redis://localhost:6379/0"
)
redis_client = redis.from_url(_redis_url, decode_responses=True)



def generate_otp(email) -> int:
    """Generate a 5-digit OTP, store in Redis with 5 min TTL, and return it. Returns None if Redis error."""
    otp = str(random.randint(10000, 99999))
    try:
        redis_client.setex(f"otp:{email}", 300, otp)  # 300 seconds = 5 minutes
        return otp
    except redis.exceptions.ConnectionError as e:
        print(f"[Redis Error] Could not store OTP: {e}")
        return None

def verify_otp(email, user_otp):
    try:
        server_otp = redis_client.get(f"otp:{email}")
        if server_otp is None:
            return False
        if str(user_otp).strip() == str(server_otp).strip():
            redis_client.delete(f"otp:{email}")
            return True
        return False
    except redis.exceptions.ConnectionError as e:
        print(f"[Redis Error] Could not verify OTP: {e}")
        return False


def send_otp(user_email: str, otp: int):
    """Send the OTP to the user's email address."""
    msg = EmailMessage()
    msg["From"] = f"BlogPy Website <{blogpy_email}>"
    msg["To"] = user_email
    msg["Subject"] = "Your OTP for Password Reset"
    msg.set_content(f"""
        Hello,

        Your OTP for resetting your BlogPy account password is: {otp}

        This code is valid for 5 minutes. If you did not request a password reset, please ignore this email.

        Best regards,
        BlogPy Team
    """)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as connection:
            connection.login(user=blogpy_email, password=app_password)
            connection.send_message(msg)
        return True, None
    except Exception as e:
        return False, str(e)



def send_contact_email(user_name: str, user_email: str, user_phone: str, user_message: str):
    """Send a contact form email. Returns (success: bool, error: str|None)."""
    # Use the same email for sending and receiving

    if not blogpy_email or not app_password:
        return False, "Email service not configured"

    msg = EmailMessage()
    msg["From"] = f"BlogPy Website <{blogpy_email}>"
    msg["To"] = blogpy_email  # Send to yourself
    msg["Reply-To"] = user_email  # So you can reply directly to the user
    msg["Subject"] = "New Contact Form Message"
    msg.set_content(f"Name: {user_name}\nEmail: {user_email}\nPhone: {user_phone}\n\nMessage:\n{user_message}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as connection:
            connection.login(user=blogpy_email, password=app_password)
            connection.send_message(msg)
        return True, None
    except Exception as e:
        return False, str(e)



def seed_categories_and_tags(app, db, Category, Tag):
    default_categories = [
        "Technology",
        "Artificial Intelligence",
        "Web Development",
        "Programming",
        "Design & UI/UX",
        "Career & Growth",
        "Science",
        "Health & Wellness",
        "Business & Finance",
        "Opinion & Essays",
        "Tutorials & Guides",
        "Project Showcases",
        "Productivity",
        "Culture & Society",
        "News & Updates",
    ]

    default_tags = [
        # Tech
        "python", "javascript", "flask", "react", "ai", "ml",
        "llm", "api", "database", "cloud", "open-source", "devops",
        # Content Type
        "tutorial", "deep-dive", "opinion", "beginner", "advanced",
        "case-study", "review", "guide", "interview",
        # Career & Life
        "career", "productivity", "mental-health", "learning",
        "students", "freelancing", "remote-work",
        # General
        "trending", "finance", "startup", "research",
        "tools", "resources", "community", "writing",
    ]
    with app.app_context():
        for name in default_categories:
            exists = db.session.execute(
                db.select(Category).where(Category.name == name)
            ).scalar()
            if not exists:
                db.session.add(Category(name=name))

        for name in default_tags:
            exists = db.session.execute(
                db.select(Tag).where(Tag.name == name)
            ).scalar()
            if not exists:
                db.session.add(Tag(name=name))

        db.session.commit()

