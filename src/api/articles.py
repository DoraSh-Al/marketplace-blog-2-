from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.models.article import Article
from src.models.category import Category
from src.models.database import get_db
from src.models.deleted_article import DeletedArticle
from src.schemas.article import ArticleOut, ArticleUpdate
from src.utils.s3 import upload_image

router = APIRouter(prefix="/articles", tags=["articles"])

@router.get("/", response_model=List[ArticleOut])
def get_articles(
    db: Session = Depends(get_db),
    search: str = None,
    category_id: int = None,
    page_number: int = 1,
    page_size: int = 10
):
    query = db.query(Article)
    if search:
        query = query.filter(
            func.to_tsvector('russian', Article.title + ' ' + Article.content).match(search, postgresql_regconfig='russian')
        )
    if category_id:
        query = query.filter(Article.category_id == category_id)
    articles = query.offset((page_number - 1) * page_size).limit(page_size).all()
    return articles

@router.post("/", response_model=ArticleOut, operation_id="create_new_article")
async def create_article(
    title: str = Form(...),
    content: str = Form(...),
    category_id: int = Form(...),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    try:
        if not db.query(Category).filter(Category.id == category_id).first():
            raise HTTPException(status_code=404, detail="Category not found")

        image_url = None
        if image:
            if not image.content_type.startswith("image/"):
                raise HTTPException(status_code=400, detail="Only images are allowed")
            image_url = await upload_image(image)

        db_article = Article(
            title=title,
            content=content,
            category_id=category_id,
            image_url=image_url
        )
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@router.patch("/{id}", response_model=ArticleOut)
def update_article(id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    update_data = article.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_article, key, value)
    db_article.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_article)
    return db_article

@router.delete("/{id}")
def delete_article(id: int, db: Session = Depends(get_db)):
    db_article = db.query(Article).filter(Article.id == id).first()
    if not db_article:
        raise HTTPException(status_code=404, detail="Article not found")
    deleted_article = DeletedArticle(article_id=id)
    db.add(deleted_article)
    db.delete(db_article)
    db.commit()
    return {"msg": "Article deleted"}
