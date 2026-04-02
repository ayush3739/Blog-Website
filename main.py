from datetime import date,datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request, session
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import login_user, LoginManager, current_user, logout_user, login_required
from models import db, BlogPost, User, Like, BookMark, Category, Tag, Comments, post_tags,NewsletterSubs
from sqlalchemy import or_, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload
from functools import wraps
from flask import jsonify
from flask_wtf.csrf import generate_csrf
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm,RegisterForm,LoginForm,CommentForm,ProfileForm,newsletterForm,reset_emailForm,Password_Form,OTP_Form
import os , bleach
import math
import time
from dotenv import load_dotenv
from utils import send_contact_email, seed_categories_and_tags,generate_otp,verify_otp,send_otp

load_dotenv('.env')

def admin_only(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            return abort(403)
        return f(*args,**kwargs)
    return decorated_function

# On Vercel (Linux, read-only FS except /tmp), use /tmp for SQLite.
# Locally, use Flask's default instance/ folder so existing data is picked up.
if os.getenv('VERCEL'):
    _instance_path = '/tmp'
    app = Flask(__name__, instance_path=_instance_path)
else:
    app = Flask(__name__)
    _instance_path = app.instance_path
    os.makedirs(_instance_path, exist_ok=True)
app.config['SECRET_KEY'] = os.getenv('secret_key', 'fallback_secret')
app.config['CKEDITOR_SERVE_LOCAL'] = True 
app.config['CKEDITOR_PKG_TYPE'] = 'standard' 
app.config['CKEDITOR_CONFIG'] = {'versionCheck': False} 
app.config['SESSION_COOKIE_SECURE'] = os.getenv('FLASK_ENV', 'development') == 'production'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager=LoginManager()
login_manager.init_app(app)

# Vercel Upstash may expose REDIS_URL or REDIS_KV_URL.
_redis_storage_uri = (
    os.getenv("REDIS_URL") or
    os.getenv("REDIS_KV_URL") or
    "memory://"
)

limiter=Limiter(key_func=get_remote_address,
                app=app,
                default_limits=["60 per minute"],
                storage_uri=_redis_storage_uri,
                )

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None



# Neon/Vercel integrations may expose one of several DB URL env vars.
_sqlite_fallback = f"sqlite:///{_instance_path}/posts.db"
_db_uri = (
    os.getenv("NEON_DATABASE_URL") or
    os.getenv("NEON_POSTGRES_URL") or
    os.getenv("POSTGRES_URL") or
    os.getenv("POSTGRES_PRISMA_URL") or
    os.getenv("DATABASE_URL") or
    _sqlite_fallback
)
# SQLAlchemy requires 'postgresql://' not 'postgres://'
if _db_uri.startswith("postgres://"):
    _db_uri = _db_uri.replace("postgres://", "postgresql://", 1)


app.config['SQLALCHEMY_DATABASE_URI'] = _db_uri
db.init_app(app)


# Flask-Migrate setup
migrate = Migrate(app, db)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=True,
                    base_url=None)

load_dotenv(".env")  


with app.app_context():
    try:
        db.create_all()
        # Seed categories and tags after tables are created
        seed_categories_and_tags(app, db, Category, Tag)
    except SQLAlchemyError as e:
        app.logger.exception("Database initialization failed during startup: %s", e)


@app.route('/register',methods=["GET","POST"])
@limiter.limit("5 per minute")
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        result=db.session.execute(db.select(User).where(User.email==email))
        user=result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        hash_and_salted_pass=generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        new_user=User(
            email=form.email.data,
            password=hash_and_salted_pass,
            name=form.name.data
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for('get_all_posts'))

    return render_template("register.html",form=form,logged_in=current_user.is_authenticated)


@app.route('/login',methods=["GET","POST"])
@limiter.limit("5 per minute")
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        result=db.session.execute(db.select(User).where(User.email==email))
        user=result.scalar()
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('login'))
        
        elif not check_password_hash(user.password,password):
            flash("Password incorrect, please try again.")
            return redirect(url_for('login'))
        
        else:
            login_user(user)
            return redirect(url_for('get_all_posts',logged_in=True))

    return render_template("login.html",form=form,logged_in=current_user.is_authenticated)

@app.route('/forgot-password', methods=["GET", "POST"])
@limiter.limit("5 per minute,20 per hour")
def forgot_pass():
    form = reset_emailForm()
    if form.validate_on_submit():
        email = form.email.data
        otp = generate_otp(email)
        if otp is None:
            flash("OTP service is temporarily unavailable. Please try again later.", "danger")
            return redirect(url_for('forgot_pass')) 
        send_otp(user_email=email, otp=otp)
        flash("An OTP has been sent to your email.", "info")
        return redirect(url_for('verify_otp_route', email=email))
    return render_template("forgot_password.html", form=form)

@app.route('/verify-password', methods=["GET", "POST"])
@limiter.limit("5 per minute,20 per hour")
def verify_otp_route():
    email = request.args.get('email')
    if not email:
        flash("Missing email for OTP verification.", "danger")
        return redirect(url_for('forgot_pass'))
    form = OTP_Form()
    if form.validate_on_submit():
        user_otp = form.otp.data
        if verify_otp(email=email, user_otp=user_otp):
            session['reset_email'] = email
            flash("OTP verified. Please reset your password.", "success")
            return redirect(url_for('reset_password', email=email))
        else:
            flash("Invalid or expired OTP. Please try again.", "danger")
            return redirect(url_for('verify_otp_route', email=email))
    return render_template("verify_otp.html", form=form, email=email)

@app.route('/reset-password', methods=["GET", "POST"])
@limiter.limit("5 per minute,20 per hour")
def reset_password():
    email = request.args.get('email')
    # Only allow if session['reset_email'] matches
    if not email or session.get('reset_email') != email:
        flash("Unauthorized or expired password reset link. Please try again.", "danger")
        return redirect(url_for('forgot_pass'))
    form = Password_Form()
    user = db.session.execute(db.select(User).where(User.email == email)).scalar_one_or_none()
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for('login'))
    if form.validate_on_submit():
        hash_and_salted_pass = generate_password_hash(
            form.new_pass.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        user.password = hash_and_salted_pass
        db.session.commit()
        session.pop('reset_email', None)
        flash("Password updated successfully. Please log in.", "success")
        return redirect(url_for('login'))
    return render_template("reset_password.html", form=form)
        

        


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/favicon.ico')
def favicon():
    return redirect(url_for('static', filename='assets/favicon.ico'), code=301)



# Global storage for caching trending posts and category IDs
trending_cache = {"posts": [], "last_updated": 0}
category_id_cache = {}
TRENDING_CACHE_TTL = 900  # 15 minutes in seconds

@app.route('/')
def get_all_posts():
    result = db.paginate(db.select(BlogPost).order_by(BlogPost.id.desc()), per_page=10)
    
    global trending_cache, category_id_cache
    current_time = time.time()
    
    # Update the cache if it's empty or 15 minutes have passed
    if not trending_cache["posts"] or (current_time - trending_cache["last_updated"] > TRENDING_CACHE_TTL):
        top_posts = db.session.execute(
            db.select(BlogPost).order_by(BlogPost.like_count.desc().nullslast(), BlogPost.id.desc()).limit(3)
        ).scalars().all()
        
        # Store as dictionaries to prevent SQLAlchemy "DetachedInstanceError" when the DB session closes
        trending_cache["posts"] = [
            {
                "id": p.id,
                "title": p.title,
                "subtitle": p.subtitle,
                "date": p.date,
                "read_time": p.read_time,
                "category": {"name": p.category.name} if p.category else None
            } for p in top_posts
        ]
        trending_cache["last_updated"] = current_time

    trending_posts = trending_cache["posts"]

    # Use cached category IDs or fetch them once if the cache is empty
    if not category_id_cache:
        categories = db.session.execute(
            db.select(Category).where(Category.name.in_(['Web Development', 'Design & UI/UX', 'Opinion & Essays']))
        ).scalars().all()
        category_id_cache.update({c.name: c.id for c in categories})
    
    dev_category_id = category_id_cache.get('Web Development')
    design_category_id = category_id_cache.get('Design & UI/UX')
    opinion_category_id = category_id_cache.get('Opinion & Essays')
    newsletter_form = newsletterForm()

    # AJAX request — return only the posts partial, not the full page
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(
            "_posts.html",
            all_posts=result,
            trending_posts=trending_posts,
            logged_in=current_user.is_authenticated,
            dev_category_id=dev_category_id,
            design_category_id=design_category_id,
            opinion_category_id=opinion_category_id,
            newsletter_form =newsletter_form
        )
    return render_template(
        "index.html",
        all_posts=result,
        trending_posts=trending_posts,
        logged_in=current_user.is_authenticated,
        dev_category_id=dev_category_id,
        design_category_id=design_category_id,
        opinion_category_id=opinion_category_id,
        newsletter_form = newsletter_form
    )


@app.route('/all-posts')
@limiter.limit("10 per minute", methods=["GET","POST"])
def all_posts():
    # Get parameters
    page = request.args.get('page', 1, type=int)
    q = request.args.get('q', '', type=str)
    sort_by = request.args.get('sort', 'newest', type=str)  
    category_id = request.args.get('category', type=int)
    tag_id = request.args.get('tag', type=int)
   
    # ...rest of your query logic...  

    # Base query
    query = db.select(BlogPost)   

    # Apply search filter
    if q:
        search_term = f"%{q}%"
        query = query.where(or_(
            BlogPost.title.ilike(search_term),
            BlogPost.subtitle.ilike(search_term)
        ))    

    # Apply sorting
    if sort_by == 'oldest':
        query = query.order_by(BlogPost.id.asc())
    elif sort_by == 'likes':
        query = query.order_by(BlogPost.like_count.desc().nullslast(), BlogPost.id.desc())
    else:
        query = query.order_by(BlogPost.id.desc()) # Default to newest

    if category_id:
        query = query.where(BlogPost.category_id == category_id)
    if tag_id:
        query = query.join(BlogPost.tags).where(Tag.id == tag_id)
        
    # Pagination
    posts = db.paginate(query, page=page, per_page=10)
    
    return render_template(
        "all-posts.html",
        posts=posts,
        q=q,
        sort=sort_by,
        logged_in=current_user.is_authenticated,
        Category=Category,
        Tag=Tag
    )



@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@limiter.limit("10 per minute", methods=["POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost,post_id)

    if not requested_post:
        abort(404)

    
    if current_user.is_authenticated:
        existing_like = db.session.execute(
            db.select(Like).where(
                Like.user_id == current_user.id,
                Like.post_id == post_id
            )
        ).scalar_one_or_none()        

        existing_bookmark=db.session.execute(
            db.select(BookMark).where(BookMark.user_id == current_user.id,BookMark.post_id == post_id)
        ).scalar_one_or_none()

        user_liked = existing_like is not None
        user_marked = existing_bookmark is not None
    else:
        user_liked = False
        user_marked = False
    page = request.args.get('page',1,type=int)
    comments_pagination = db.paginate(
        db.select(Comments)
        .options(selectinload(Comments.comment_author),
                 selectinload(Comments.replies).selectinload(Comments.comment_author))
        .where(Comments.post_id == post_id,Comments.parent_id == None),
        page=page,
        per_page=3
    )
    comments = comments_pagination.items

    comment_form = CommentForm()
 
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for('login'))
        parent_comment=None
        parent_id=comment_form.parent_id.data

        if parent_id:
            parent_id=int(parent_id)
            parent_comment=db.session.get(Comments,parent_id)
            if parent_comment and parent_comment.post_id != post_id:
                abort(400)
        clean_text=bleach.clean(
            comment_form.comment.data,
            tags = [],
            strip = True

        )
        new_comment = Comments(
                text= clean_text,
                comment_author=current_user,
                parent_post=requested_post,
                parent=parent_comment
            )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))

    # AJAX: Only return the next batch of comments (for load more)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template(
            "_comments.html",
            comments=comments,
            post=requested_post,
            form=comment_form,
            logged_in=current_user.is_authenticated,
            comments_pagination=comments_pagination
        )
    
    return render_template(
        "post.html",
        post=requested_post,
        form=comment_form,
        comments=comments,
        comments_pagination=comments_pagination,
        logged_in=current_user.is_authenticated,
        user_liked=user_liked,
        user_marked=user_marked
    )

@app.route("/new-post", methods=["GET", "POST"])
@limiter.limit("5 per minute")
@login_required
def add_new_post():
    form = CreatePostForm()
    #populate dropdown choices
    form.category.choices = [(0, "— Select a category —")] + [
        (c.id, c.name) for c in db.session.execute(db.select(Category)).scalars().all()
    ]    
    form.tags.choices = [(t.id,t.name) for t in db.session.execute(db.select(Tag)).scalars().all()]
    if form.validate_on_submit():
        body_text = form.body.data or ""
        word_count = len(body_text.split())
        read_time = max(1, math.ceil(word_count / 200))
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=body_text,
            img_url=form.img_url.data,
            author=current_user,  
            date=date.today().strftime("%B %d, %Y"),
            read_time=read_time,
            category_id = form.category.data,
        )
        db.session.add(new_post)
        selected_tags = db.session.execute(db.select(Tag).where(Tag.id.in_(form.tags.data))).scalars().all()
        new_post.tags = selected_tags
        
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    
    return render_template("make-post.html", form=form, logged_in=current_user.is_authenticated)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html',logged_in=current_user.is_authenticated, user=current_user, csrf_token=generate_csrf())

@app.route('/edit-profile', methods=["GET", "POST"])
@login_required
def edit_profile():
    user = db.get_or_404(User, current_user.id)
    form = ProfileForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data
        user.email = form.email.data
        user.bio = form.bio.data
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for("profile"))
    return render_template("edit-profile.html", form=form, logged_in=current_user.is_authenticated)

@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    # Only allow if admin or the author
    if not (current_user.is_admin or post.author_id == current_user.id):
        abort(403)

    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body,
        category = post.category_id,
        tags = [t.id for t in post.tags]
    )
    edit_form.category.choices = [
        (c.id, c.name)
        for c in db.session.execute(db.select(Category)).scalars().all()
    ]
    edit_form.tags.choices = [
        (t.id, t.name)
        for t in db.session.execute(db.select(Tag)).scalars().all()
    ]

    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        post.category_id = edit_form.category.data

        selected_tags = db.session.execute(
            db.select(Tag).where(Tag.id.in_(edit_form.tags.data))
        ).scalars().all()
        post.tags = selected_tags
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, logged_in=current_user.is_authenticated)


@app.route("/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    # Only allow if admin or the author
    if not (current_user.is_admin or post_to_delete.author_id == current_user.id):
        abort(403)
    db.session.delete(post_to_delete)
    db.session.commit()
    
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html",logged_in=current_user.is_authenticated)



from forms import ContactForm

@app.route("/contact", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        name = form.name.data.strip()
        email = form.email.data.strip()
        phone = form.phone.data.strip()
        message = form.message.data.strip()

        ok, err = send_contact_email(name, email, phone, message)
        if ok:
            flash("Your message has been sent successfully! We'll get back to you soon.", "success")
            return redirect(url_for("contact"))
        else:
            flash(f"Could not send message. {err}", "error")
            return render_template("contact.html", form=form, logged_in=current_user.is_authenticated, msg_sent=False)

    return render_template("contact.html", form=form, logged_in=current_user.is_authenticated, msg_sent=False)


@app.route("/debug/user/<int:user_id>")
@admin_only
def debug_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "user": {"id": user.id, "email": user.email, "name": user.name},
        "posts": [{"id": p.id, "title": p.title, "date": p.date} for p in user.posts],
        "post_count": len(user.posts),
    }

#like functionality
@app.route("/like/<int:post_id>",methods=["POST"])
@limiter.limit("5 per minute")
def like_toggle(post_id):
    if not current_user.is_authenticated:
        flash("You need to login to like posts.")
        return redirect(url_for('show_post', post_id=post_id))
    user_id = current_user.id

    is_ajax = request.headers.get('X-Requested-With') == "XMLHttpRequest"
    post = db.session.get(BlogPost, post_id)
    if not post:
        abort(404)

    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()
    if like:
        db.session.delete(like)
        liked = False
    else:
        like = Like(
            user_id=user_id,
            post_id=post_id
        )
        db.session.add(like)
        liked = True

    # Flush toggle first, then derive count from source of truth to avoid race drift.
    db.session.flush()
    actual_like_count = db.session.execute(
        db.select(func.count()).select_from(Like).where(Like.post_id == post_id)
    ).scalar_one()
    post.like_count = max(0, int(actual_like_count))
    db.session.commit()

    # Get updated like count
    like_count = post.like_count

    if is_ajax:
        return jsonify({"like_count": like_count, "liked": liked})
    return redirect(url_for('show_post', post_id=post_id))

@app.route("/bookmark/<int:post_id>",methods=["POST"])
@limiter.limit("5 per minute")
def bookmark_toggle(post_id):
    if not current_user.is_authenticated:
        flash("You need to login to bookmark posts.")
        return redirect(url_for('show_post', post_id=post_id))
    user_id = current_user.id

    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    bookmark = BookMark.query.filter_by(user_id=user_id, post_id=post_id).first()
    if bookmark:
        db.session.delete(bookmark)
        bookmarked = False
    else:
        book_mark = BookMark(
            user_id=user_id,
            post_id=post_id
        )
        db.session.add(book_mark)
        bookmarked = True
    db.session.commit()

    if is_ajax:
        return jsonify({"bookmarked": bookmarked})
    return redirect(url_for('show_post', post_id=post_id))

@app.route('/newsletter-subs',methods=["POST"])
@limiter.limit('5 per minute')
def news_subscriber():
    form = newsletterForm()
    if form.validate_on_submit():
        existing = db.session.execute(db.select(NewsletterSubs).where(NewsletterSubs.email == form.email.data)).scalar_one_or_none()
        if existing:
            flash("This email is already subscribed.", "warning")
            return redirect(request.referrer or url_for('get_all_posts'))
        news = NewsletterSubs(
            email=form.email.data,
            date_subscribed=datetime.utcnow()
        )
        db.session.add(news)
        db.session.commit()
        flash("You have Subscribed to the Newsletter", "success")
        return redirect(request.referrer or url_for('get_all_posts'))
    flash("Invalid email address.", "danger")
    return redirect(request.referrer or url_for('get_all_posts'))


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", logged_in=current_user.is_authenticated), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", logged_in=current_user.is_authenticated), 500


@app.errorhandler(403)
def forbidden(e):
    return render_template("404.html", logged_in=current_user.is_authenticated), 403


@app.route('/too-many-requests')
def too_many_requests_page():
    return render_template("429.html", logged_in=current_user.is_authenticated), 429

@app.errorhandler(429)
def ratelimit_handler(e):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({"error": "rate_limited", "message": "Too many requests. Please wait and try again."}), 429
    return render_template("429.html", logged_in=current_user.is_authenticated), 429



if __name__ == "__main__":
    app.run(debug=False)
