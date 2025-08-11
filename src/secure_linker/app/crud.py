from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from .models import SecureLink, Base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_secure_link(db, token, content, days, visualizations, expires_at):
    link = SecureLink(
        token=token,
        content=content,
        days=days,
        visualizations=visualizations,
        expires_at=expires_at
    )
    db.add(link)
    db.commit()
    return link


def get_secure_link(db, token):
    return db.query(SecureLink).filter(SecureLink.token == token).first()


def remove_secure_link(db, token):
    link = get_secure_link(db, token)
    if link:
        db.delete(link)
        db.commit()
    return link


def update_secure_link(db, token, content=None, days=None, visualizations=None, expires_at=None):
    link = get_secure_link(db, token)
    if link:
        if content is not None:
            link.content = content
        if days is not None:
            link.days = days
        if visualizations is not None:
            link.visualizations = visualizations
        if expires_at is not None:
            link.expires_at = expires_at
        db.commit()
    return link
