import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./rkb.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    user_id = Column(String, unique=True)
    access_token = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Page(Base):
    __tablename__ = "pages"
    id = Column(String, primary_key=True)
    name = Column(String)
    account_id = Column(Integer, ForeignKey("accounts.id"))
    page_access_token = Column(Text)
    category = Column(String)
    tasks = Column(Text)

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    message = Column(Text)
    media_path = Column(String)
    media_type = Column(String)
    status = Column(String, default="queued")
    scheduled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

class PostPage(Base):
    __tablename__ = "post_pages"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    page_id = Column(String, ForeignKey("pages.id"))
    page_name = Column(String)
    caption = Column(Text)
    status = Column(String, default="pending")
    result = Column(Text)

Base.metadata.create_all(engine)

app = FastAPI(title="RKB Page Manager")
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    db = SessionLocal()
    try:
        accounts = db.query(Account).all()
        pages = db.query(Page).all()
        posts = db.query(Post).order_by(Post.created_at.desc()).limit(100).all()
        return templates.TemplateResponse("dashboard.html", {"request": request, "accounts": accounts, "pages": pages, "posts": posts})
    finally:
        db.close()
