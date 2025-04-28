from datetime import datetime

from sqlalchemy import Column, DateTime, Integer

from src.models.base import Base


class DeletedArticle(Base):
    __tablename__ = "deleted_articles"
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, nullable=False)
    deleted_at = Column(DateTime, default=datetime.utcnow)
