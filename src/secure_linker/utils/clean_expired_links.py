import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from src.secure_linker.app.models import SecureLink

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def clean_expired_links():
    db = SessionLocal()
    now = datetime.utcnow()
    expired_links = db.query(SecureLink).filter(
        (SecureLink.expires_at < now) | (SecureLink.visualizations <= 0)
    ).all()
    count = len(expired_links)
    for link in expired_links:
        db.delete(link)
    db.commit()
    db.close()
    print(f"Eliminados {count} enlaces expirados.")

if __name__ == "__main__":
    clean_expired_links()
