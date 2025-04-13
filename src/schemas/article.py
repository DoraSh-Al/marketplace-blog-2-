from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArticleCreate(BaseModel):
    title: str
    content: str
    category_id: int

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    category_id: int
    image_url: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
