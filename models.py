from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, DateTime, Boolean
from datetime import datetime

# SQLAlchemy base and db instance
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


# Association table for BlogPost <-> Tag many-to-many
post_tags = db.Table(
    "post_tags",
    db.Column("post_id", Integer, ForeignKey("blog_posts.id"), primary_key=True),
    db.Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True)
)

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    read_time : Mapped[int] = mapped_column(Integer,default=1,nullable=False)

    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), nullable=False)
    comments=relationship("Comments",back_populates="parent_post", cascade="all, delete-orphan")
    likes=relationship("Like",back_populates="post", cascade="all, delete-orphan")
    like_count:Mapped[int] =  mapped_column(Integer, default=0, nullable=False)
    bookmarks=relationship("BookMark",back_populates="post", cascade="all, delete-orphan")

    category_id : Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'),nullable=True)
    category = relationship('Category',back_populates="posts")
    tags = relationship('Tag', secondary=post_tags, back_populates="posts")



class User(UserMixin,db.Model):
    __tablename__ = "users"  
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    email:Mapped[str]=mapped_column(String(100),unique=True,nullable=False)
    password:Mapped[str]=mapped_column(String(100),)
    name:Mapped[str]=mapped_column(String(100),nullable=False)
    bio:Mapped[str] = mapped_column(String(1000),nullable=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at : Mapped[datetime] = mapped_column(DateTime, nullable= False, default= datetime.utcnow)
   
    posts = relationship("BlogPost", back_populates="author")
    comments=relationship("Comments",back_populates="comment_author")
    likes=relationship("Like",back_populates="user")
    bookmarks=relationship("BookMark",back_populates="user")

class Like(db.Model):
    __tablename__="likes"
    user_id:Mapped[int] =mapped_column(Integer,ForeignKey("users.id"),primary_key=True)
    post_id:Mapped[int] = mapped_column(Integer,ForeignKey("blog_posts.id"),primary_key=True)
    user = relationship("User",back_populates="likes")
    post = relationship("BlogPost",back_populates="likes")

class BookMark(db.Model):
    __tablename__ = "bookmarks"
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey('users.id'),primary_key=True)
    post_id:Mapped[int] = mapped_column(Integer,ForeignKey("blog_posts.id"),primary_key=True)
    user=relationship("User",back_populates="bookmarks")
    post=relationship("BlogPost",back_populates="bookmarks")

class Category(db.Model):
    __tablename__ = "categories"
    id : Mapped[int] =mapped_column(Integer,primary_key=True)
    name : Mapped[String] = mapped_column(String(100),unique=True,nullable=False)
    posts=relationship("BlogPost",back_populates="category")

class Tag(db.Model):
    __tablename__ = "tags"
    id : Mapped[int] =mapped_column(Integer,primary_key=True)
    name : Mapped[String] = mapped_column(String(50),unique=True,nullable=False)
    posts=relationship("BlogPost", secondary=post_tags, back_populates="tags")

class Comments(db.Model):
    __tablename__="comments"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    parent_id:Mapped[int] = mapped_column(Integer,ForeignKey("comments.id"),nullable=True)
    author_id: Mapped[int] = mapped_column(Integer,ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    parent= relationship("Comments", remote_side="Comments.id",back_populates="replies")
    replies= relationship("Comments", back_populates="parent",cascade="all, delete-orphan")
    post_id:Mapped[int]=mapped_column(Integer,ForeignKey("blog_posts.id"))
    parent_post=relationship("BlogPost",back_populates="comments")
    text:Mapped[str]=mapped_column(String(300),nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


class NewsletterSubs(db.Model):
    __tablename__ = "newsletter_subs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    date_subscribed: Mapped[DateTime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
