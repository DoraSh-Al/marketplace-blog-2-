from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from src.models.base import Base


class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    content = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
