from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta

Base = declarative_base()

class SecureLink(Base):
    __tablename__ = "secure_links"
    token = Column(String, primary_key=True, index=True)
    content = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    visualizations = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)

    def is_expired(self):
        return datetime.utcnow() > self.expires_at or self.visualizations <= 0

    def decrement_visualizations(self, db):
        if self.visualizations > 0:
            self.visualizations -= 1
            db.commit()
    def decrement_days(self, db):
        if self.days > 0:
            self.days -= 1
            db.commit()
