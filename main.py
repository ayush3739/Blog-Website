from datetime import date, datetime
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor,CKEditorField
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Boolean
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import CreatePostForm,RegisterForm,LoginForm,CommentForm
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv



def admin_only(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            return abort(403)
        return f(*args,**kwargs)
    return decorated_function

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('secret_key')
app.config['CKEDITOR_SERVE_LOCAL'] = True 
app.config['CKEDITOR_PKG_TYPE'] = 'standard' 
app.config['CKEDITOR_CONFIG'] = {'versionCheck': False} 
ckeditor = CKEditor(app)
Bootstrap5(app)

login_manager=LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Return None if user not found; avoid aborting from user loader
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")

    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments=relationship("Comments",back_populates="parent_post")
    
class User(UserMixin,db.Model):
    __tablename__ = "users"  
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    email:Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
    password:Mapped[str]=mapped_column(String(100),)
    name:Mapped[str]=mapped_column(String(100),nullable=False)
    # Admin flag (False by default). Manage via ops tools (no UI self-promotion).
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
   
    posts = relationship("BlogPost", back_populates="author")
    comments=relationship("Comments",back_populates="comment_author")

class Comments(db.Model):
    __tablename__="comments"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")


    post_id:Mapped[int]=mapped_column(Integer,ForeignKey("blog_posts.id"))
    parent_post=relationship("BlogPost",back_populates="comments")
    text:Mapped[str]=mapped_column(String(300),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

load_dotenv(".env")  

with app.app_context():
    db.create_all()


def send_contact_email(user_name: str, user_email: str, user_phone: str, user_message: str):
    from_email = os.getenv("email")
    app_password = os.getenv("pass")
    to_email = os.getenv("to_email") 
    if not from_email or not app_password or not to_email:
        return False, "Email service not configured"

    msg = EmailMessage()
    msg["From"] = f"Blog Website <{from_email}>"
    msg["To"] = to_email
    msg["Reply-To"] = user_email
    msg["Subject"] = "New Contact Form Message"
    msg.set_content(f"Name: {user_name}\nEmail: {user_email}\nPhone: {user_phone}\n\nMessage:\n{user_message}")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587, timeout=10) as connection:
            connection.starttls()
            connection.login(user=from_email, password=app_password)
            connection.send_message(msg)
        return True, None
    except Exception as e:
        return False, str(e)


@app.route('/register',methods=["GET","POST"])
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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route('/')
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts,logged_in=current_user.is_authenticated)


@app.route("/post/<int:post_id>",methods=["GET","POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comments = db.session.execute(db.select(Comments).where(Comments.post_id == post_id)).scalars().all()
    comment_form=CommentForm()
    if comment_form.validate_on_submit():
        if not current_user.is_authenticated:
            flash("You need to login or register to comment.")
            return redirect(url_for('login'))
        new_comment=Comments(
            text=comment_form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
            
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for('show_post', post_id=post_id))

    return render_template("post.html", post=requested_post,form=comment_form,comments=comments,logged_in=current_user.is_authenticated)


@app.route("/new-post", methods=["GET", "POST"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,  
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form, logged_in=current_user.is_authenticated)


@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
@admin_only
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True, logged_in=current_user.is_authenticated)


@app.route("/delete/<int:post_id>")
@admin_only
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html",logged_in=current_user.is_authenticated)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        if not current_user.is_authenticated:
            flash("You need to login or register to send a message.")
            return redirect(url_for("login"))
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        message = request.form.get("message", "").strip()

        ok, err = send_contact_email(name, email, phone, message)
        if ok:
            flash("Message sent.")
            return render_template("contact.html", logged_in=current_user.is_authenticated, msg_sent=True)
        else:
            flash(f"Could not send message. {err}")
            return render_template("contact.html", logged_in=current_user.is_authenticated, msg_sent=False)

    return render_template("contact.html", logged_in=current_user.is_authenticated, msg_sent=False)

@app.route("/debug/user/<int:user_id>")
@admin_only
def debug_user(user_id):
    user = db.get_or_404(User, user_id)
    return {
        "user": {"id": user.id, "email": user.email, "name": user.name},
        "posts": [{"id": p.id, "title": p.title, "date": p.date} for p in user.posts],
        "post_count": len(user.posts),
    }



if __name__ == "__main__":
    app.run(debug=True)
