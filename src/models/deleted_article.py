from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

from src.models.base import Base


class DeletedArticle(Base):
    __tablename__ = "deleted_articles"
    article_id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)  # Должно быть!
    content = Column(String, nullable=False)  # Должно быть!
    category_id = Column(Integer, ForeignKey("categories.id"))
    image_url = Column(String, nullable=True)
    deleted_at = Column(DateTime, default=datetime.utcnow)
