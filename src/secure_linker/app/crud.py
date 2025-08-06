from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from .models import SecureLink, Base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/securelinker")
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
